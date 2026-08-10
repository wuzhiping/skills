# Obtaining AIFE env values via the email-code flow

When a task needs credentials from the AIFE platform and no current values are available, obtain them through AIFE's two-step email-code API. Never invent values, never reuse old tokens, and never call the protected resource until both steps have succeeded.

> **Verified against the live endpoint, Aug 2026:** POSTing `{email}` to this URL DOES dispatch the verification code and returns HTTP 200 with body `"邮件已发送"`. Step 1 is therefore a single API call on the same `/oauth2/aife_tokens` endpoint — you do NOT need a separate admin trigger / out-of-band request. A previous version of this skill claimed POST `{email}` returns 500 `没有code`; that was wrong.

## The two API calls

Step 1 and Step 2 share the same URL `https://abc.feg.com.tw/oauth2/aife_tokens` and both accept and return JSON. Both are unauthenticated — possession of the verification code mailed to the user is the only proof of identity.

**Step 1 — request a verification code:**

POST `{email}` to this URL. The server triggers the verification email and returns HTTP 200 with body `"邮件已发送"`. First attempt can occasionally return a transient HTTP 500 `没有code` (cold-start race on the upstream mailer); one retry with the identical payload usually returns 200.

```
POST https://abc.feg.com.tw/oauth2/aife_tokens
Content-Type: application/json

{"email": "<user@example.com>"}
```

Wait for the 6-digit code to arrive in the user's mailbox before proceeding to Step 2. The code is only valid for a short window (typically ~10 minutes).

**Step 2 — exchange the code for env values:**

```
POST https://abc.feg.com.tw/oauth2/aife_tokens
Content-Type: application/json

{"email": "<user@example.com>", "code": "<6-digit code>"}
```

On success (HTTP 200), the response is a **nested JSON object**, not a flat `KEY=value` map. The verified observed shape (Aug 2026) is:

```json
{
  "user": { "uid": "<string>" },
  "hasura": {
    "x-hasura-admin-secret": "<string>",
    "server": "<host:port>/v1/graphql"
  }
}
```

Before persisting anything, flatten the response into env-style keys by walking to every leaf and using the dotted path as the env-var name, upper-snake-cased, prefixed with `AIFE_`. For the example above that becomes:

- `AIFE_USER_UID`
- `AIFE_HASURA_X_HASURA_ADMIN_SECRET`
- `AIFE_HASURA_SERVER`

Flat-response example the skill previously claimed (all keys are env-var names directly):

```json
{
  "AIFE_CLIENT_ID": "...",
  "AIFE_CLIENT_SECRET": "...",
  "AIFE_BASE_URL": "https://..."
}
```

That shape is also accepted: if every top-level key already starts with `AIFE_` and every value is a string, write each as `KEY=value` directly. If the response is nested, flatten with the leaf-path rule above. Anything else (arrays at the top level, mixed scalar/object values, empty object) -> stop and surface to the user per the failure table.

> **Caution on default-looking values:** if `x-hasura-admin-secret` looks like a shared default (e.g. `hasuraPassw0rd`, `admin`, `changeme`) or `server` is an RFC1918 address (e.g. `10.x.x.x`, `192.168.x.x`, `172.16-31.x.x`), do not auto-save. Show the user the leaf-path + prefix/suffix of the value and ask explicitly whether they want this written to disk. These may be sandbox defaults rather than the user's real credentials.

## The five-step flow

1. **Require an email from the user before doing anything else.** Do NOT call step 2 until the user has provided an email address AND a freshly-issued 6-digit code for this session. Read `~/.hermes/.env` for `AIFE_EMAIL` only to use as a suggested default; never auto-use it. If the file has `AIFE_EMAIL`, show it to the user and ask explicitly whether to reuse it or use a different one. If the file has no `AIFE_EMAIL`, ask for one from scratch. If the user does not provide one, stop — do not invent a placeholder, do not call any endpoint. Once the user provides (or confirms) an email, persist it as `AIFE_EMAIL` in `~/.hermes/.env` (one-line exception to the "ask before saving" rule — the email is not a secret, it's a delivery address). The code itself is NEVER persisted under any circumstances.
2. **Trigger the verification email.** POST `{"email": ...}` to `/oauth2/aife_tokens`. Expect HTTP 200 `"邮件已发送"`. If the first attempt returns 5xx (typically `没有code`), retry once with the identical payload — that's a transient cold-start race, not a contract violation. Then wait for the user to receive the 6-digit code by mail before proceeding.
3. **Ask for the code.** Use `clarify` open-ended. Remind the user to paste only the digits, not the surrounding email. Don't read it out loud or echo it back in logs.
4. **Call step 2.** POST `{"email": ..., "code": ...}`. On 2xx, you now have the env dict (flat or nested — see "Step 2" above). On 4xx, the code is wrong or expired — go back to step 2 of this flow (re-obtain a code), never retry step 4 with the same code. On 5xx, retry once with the same code, then surface the error.
5. **Ask before saving.** The token values are sensitive. Use `clarify` single-select with two choices: "save to `~/.hermes/.env`" or "use this call only". Do not auto-save. If the user chooses save, write each flattened key/value pair as its own `KEY=value` line in `~/.hermes/.env` via `env-file-persistence`'s `persist_env_var.py`. If they choose use-once, hold the values in memory for the rest of this turn only and tell the user they will need to repeat the flow next time. **Always surface default-looking secrets and RFC1918 endpoints before the save question**, so the user can choose save vs use-once with full information.

## Storage details

**Where:** `~/.hermes/.env` for both `AIFE_EMAIL` (always) and the flattened env dict from step 4 (only with user opt-in). The file is shared across projects — that's the point.

**Permissions:** Before the first write of a session, verify the storage is locked down to the current user only. The mechanism depends on the platform:

- **Linux / macOS:** the directory `~/.hermes` must be `0o700` and the file `~/.hermes/.env` must be `0o600`. Check with `os.stat().st_mode & 0o777`; if permissions are wider, refuse and tell the user to tighten them (`chmod 700 ~/.hermes; chmod 600 ~/.hermes/.env`) rather than silently loosening later.
- **Windows (NTFS):** POSIX mode bits from `os.stat` are meaningless — `os.chmod` only flips the read-only flag and does not touch the ACL. Use `icacls <path>` (or `subprocess.run(["icacls", path])`) and verify the DACL contains no `Everyone`, `Users`, or `Authenticated Users` entries with read/write access. If it does, refuse to write and tell the user to tighten via `icacls <path> /inheritance:r /grant <USER>:(OI)(CI)F "SYSTEM:(OI)(CI)F" "Administrators:(OI)(CI)F"`. The `0o700 / 0o600` rule does not apply on Windows — do not refuse writes purely because `os.stat` reports `0o777` on an NTFS volume.

**Format:** Each flattened key from the Step 2 response becomes one `KEY=value` line, in the order the server returned them, with the existing `AIFE_EMAIL` line preserved at the top. Delegate to `env-file-persistence` for each line — its four rules (anchored regex, preserve other keys, refuse empty values, atomic write for tokens) already handle every edge case.

**What never goes to disk without explicit consent:** `code` (the verification code), and every value returned by step 4 until the user has opted in. If you logged the full response body for debugging, redact it from the conversation transcript before persisting anything derived from it.

## What to do on each failure

| Symptom | Cause | Action |
|---|---|---|
| Step 4 returns 4xx with "无效的code:..." | Wrong digits or expired | Go re-obtain a fresh code from the user; never retry step 4 with the same code |
| Step 4 returns 4xx with "code expired" | Window closed (>10 min usually) | Go re-obtain a fresh code from the user |
| Step 4 returns 5xx | Server issue | Retry once with the same code, then surface the error |
| Step 4 returns 2xx but body is empty / not parseable JSON | Network truncation or upstream bug | Stop, show the user the raw body (redact token values), ask how to proceed |
| Step 4 returns 2xx with nested JSON containing default-looking secrets or RFC1918 endpoints | Possibly sandbox / staging credentials | Surface to user with leaf-paths + prefix/suffix BEFORE the save question |
| Step 4 returns 2xx but body is an array or has unexpected shape | API contract drift | Stop, show the user the body, ask them how to proceed |
| `POST {email}` to this URL returns 500 `没有code` on the FIRST try | Transient cold-start race on the upstream mailer | Retry once with the identical payload; second attempt usually returns 200 `"邮件已发送"` |

Never loop the whole flow without the user. Never retry step 4 with the same code — it will keep failing and burn the user's patience. Never POST `{email}` to `/oauth2/aife_tokens` expecting a code in return.

## Anti-patterns

- **Don't skip the user-provided code.** There is no shortcut path that returns a token without a code, and there is no endpoint path that triggers the code email — the code must come from the user.
- **Don't assume this endpoint does not send mail.** Verified Aug 2026: POST `{email}` to `/oauth2/aife_tokens` returns HTTP 200 `"邮件已发送"`. A previous version of this skill claimed otherwise; that was wrong. Step 1 IS a one-call API trigger.
- **Don't log the code or any token value in full.** Show the prefix/suffix only ("saved `AIFE_HASURA_X_HASURA_ADMIN_SECRET` ending `...7f3a`"). Treat the response body as a secret from the moment it arrives.
- **Don't write the response before asking.** Always confirm save-first vs use-once, and surface default-looking secrets first.
- **Don't reuse yesterday's `AIFE_*` values as if they were current.** Tokens expire; the response is only valid for whatever the API said it was valid for.
- **Don't call the AIFE resource with the values until the user has approved saving or confirmed use-once.** The flow ends at the response, not at the first successful resource call.
- **Don't apply the POSIX `0o700/0o600` check on Windows.** NTFS uses ACLs; the rule will false-positive on every Windows machine and refuse every write.

## Reading order on each call

1. Per-call override from the user's current message — always wins. (The user can paste a fresh env dict directly and skip the flow.)
2. `~/.hermes/.env` keys `AIFE_*` — read-only, do not auto-trust if older than the user expects; ask "use the saved AIFE values, or refresh?"
3. Run the full code -> exchange flow (steps 1-5 above).

The saved values are a convenience, not an assumption. Each new task should ask before reusing them, because they may have expired.

## Verification

After step 4 returns a dict and the user opts in to saving:

```python
import os, subprocess
# Confirm the file exists and contains every flattened key from the response
def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = f"{prefix}{k}" if not prefix else f"{prefix}_{k}"
        if isinstance(v, dict):
            out.update(flatten(v, key))
        else:
            out[key.upper()] = str(v)
    return out

saved = {}
with open(os.path.expanduser("~/.hermes/.env")) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            saved[k] = v

response_dict = {...}  # the parsed JSON from step 4
flat = flatten(response_dict)
prefixed = {f"AIFE_{k}" if not k.startswith("AIFE_") else k: v for k, v in flat.items()}
missing = [k for k in prefixed if k not in saved]
assert not missing, f"missing keys after save: {missing}"
```

Then run `env-file-persistence/scripts/persist_env_var.py ~/.hermes/.env <first_flattened_key> --print` as a smoke check; exit 0 means the first variable round-tripped. Spot-check the file's permissions still read `0o600` on POSIX, or `icacls` shows no `Everyone/Users` entries on Windows.

If the subsequent resource call fails with 401/403, the saved values are stale or rejected — re-run the flow from step 1 rather than trying to "fix" individual keys.