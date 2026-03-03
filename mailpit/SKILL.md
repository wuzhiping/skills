---
name: mailpit
description: 当您需要发送电子邮件时，使用 Mailpit HTTP API 发送邮件，邮件保留在 Mailpit 中
---

## Trigger

Use this skill when user asks to:
- send email
- 发邮件
- 邮件通知
- email someone
- notify via email

---

## Parameters

```json
{
  "type": "object",
  "properties": {
    "from_email": { "type": "string" },
    "from_name": { "type": "string" },
    "to": {
      "type": "array",
      "items": { "type": "string" }
    },
    "cc": {
      "type": "array",
      "items": { "type": "string" }
    },
    "bcc": {
      "type": "array",
      "items": { "type": "string" }
    },
    "subject": { "type": "string" },
    "text": { "type": "string" },
    "html": { "type": "string" },
    "attachments": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["from_email", "to", "subject"]
}
```

---

# 发送邮件

## Python
```python
import requests
import base64
import os

API_URL = "http://10.17.1.26:8025/api/v1/send"

def encode_file(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def execute(arguments):

    payload = {
        "From": {
            "Email": arguments["from_email"],
            "Name": arguments.get("from_name", "")
        },
        "To": [{"Email": email} for email in arguments["to"]],
        "Subject": arguments["subject"]
    }

    if arguments.get("text"):
        payload["Text"] = arguments["text"]

    if arguments.get("html"):
        payload["HTML"] = arguments["html"]

    if arguments.get("cc"):
        payload["Cc"] = [{"Email": email} for email in arguments["cc"]]

    if arguments.get("bcc"):
        payload["Bcc"] = arguments["bcc"]

    if arguments.get("attachments"):
        payload["Attachments"] = []
        for path in arguments["attachments"]:
            if os.path.exists(path):
                payload["Attachments"].append({
                    "Content": encode_file(path),
                    "ContentType": "application/octet-stream",
                    "Filename": os.path.basename(path)
                })

    response = requests.post(
        API_URL,
        json=payload,
        headers={
            "accept": "application/json",
            "content-type": "application/json"
        }
    )

    return {
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "response": response.text
    }
```
---


