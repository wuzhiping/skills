---
name: fde-rd
description: "Delegate coding to OpenCode CLI with Wrapped Command RD & DD."
---

# RD && DD CLI
Use RD && DD as an autonomous coding worker orchestrated by Hermes terminal/process tools. OpenCode is a provider-agnostic, open-source AI coding agent with a TUI(DD) and CLI(RD).

## When to Use



## Prerequisites

- `pty=true` for interactive DD sessions


## One-Shot Tasks

Use `RD` for bounded, non-interactive tasks:

```
terminal(command="RD <> <> 'Add retry logic to API calls and update tests'")
```

Attach context files with `-f`:

```
terminal(command="RD <> <> 'Review this config for security issues' -f config.yaml -f .env.example")
```

Show model thinking with `--thinking`:

```
terminal(command="RD <> <> 'Debug why tests fail in CI' --thinking")
```

Force a specific model:

```
terminal(command="RD <> <> 'Refactor auth module' --model openrouter/anthropic/claude-sonnet-4")
```

## Interactive DD Sessions (Background)

For iterative work requiring multiple exchanges, start the TUI in background:

```
terminal(command="DD <> <>", background=true, pty=true)
# Returns session_id

# Send a prompt
process(action="submit", session_id="<id>", data="Implement OAuth refresh flow and add tests")

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send follow-up input
process(action="submit", session_id="<id>", data="Now add error handling for token expiry")

# Exit cleanly — Ctrl+C
process(action="write", session_id="<id>", data="\x03")
# Or just kill the process
process(action="kill", session_id="<id>")
```

**Important:** Do NOT use `/exit` — it is not a valid OpenCode command and will open an agent selector dialog instead. Use Ctrl+C (`\x03`) or `process(action="kill")` to exit.

### TUI Keybindings

| Key | Action |
|-----|--------|
| `Enter` | Submit message (press twice if needed) |
| `Tab` | Switch between agents (build/plan) |
| `Ctrl+P` | Open command palette |
| `Ctrl+X L` | Switch session |
| `Ctrl+X M` | Switch model |
| `Ctrl+X N` | New session |
| `Ctrl+X E` | Open editor |
| `Ctrl+C` | Exit OpenCode |

### Resuming DD Sessions

After exiting, DD prints a session ID. Resume with:

```
terminal(command="DD <> <> -c", background=true, pty=true)  # Continue last session
terminal(command="DD <> <> -s ses_abc123", background=true, pty=true)  # Specific session
```

## Common Flags

| Flag | Use |
|------|-----|
| `--continue` / `-c` | Continue the last OpenCode session |
| `--session <id>` / `-s` | Continue a specific session |
| `--agent <name>` | Choose OpenCode agent (build or plan) |
| `--model provider/model` | Force specific model |
| `--format json` | Machine-readable output/events |
| `--file <path>` / `-f` | Attach file(s) to the message |
| `--thinking` | Show model thinking blocks |
| `--variant <level>` | Reasoning effort (high, max, minimal) |
| `--title <name>` | Name the session |
| `--attach <url>` | Connect to a running opencode server |

## Procedure

1. Verify tool readiness:
   - `terminal(command="opencode --version")`
   - `terminal(command="opencode auth list")`
2. For bounded tasks, use `opencode run '...'` (no pty needed).
3. For iterative tasks, start `opencode` with `background=true, pty=true`.
4. Monitor long tasks with `process(action="poll"|"log")`.
5. If OpenCode asks for input, respond via `process(action="submit", ...)`.
6. Exit with `process(action="write", data="\x03")` or `process(action="kill")`.
7. Summarize file changes, test results, and next steps back to user.

## Session & Cost Management


## Pitfalls

- Interactive `DD` (TUI) sessions require `pty=true`. The `RD` command does NOT need pty.
- `/exit` is NOT a valid command — it opens an agent selector. Use Ctrl+C to exit the TUI.
- PATH mismatch can select the wrong OpenCode binary/model config.
- If OpenCode appears stuck, inspect logs before killing:
  - `process(action="log", session_id="<id>")`
- Avoid sharing one working directory across parallel OpenCode sessions.
- Enter may need to be pressed twice to submit in the TUI (once to finalize text, once to send).


## Rules

1. Prefer `RD` for one-shot automation — it's simpler and doesn't need pty.
2. Use interactive background mode only when iteration is needed.
3. For long tasks, provide progress updates from `process` logs.
4. Report concrete outcomes (files changed, tests, remaining risks).
5. Exit interactive sessions with Ctrl+C or kill, never `/exit`.