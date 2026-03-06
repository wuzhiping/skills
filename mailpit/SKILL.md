---
name: mailpit
description: 当您需要发送电子邮件时，使用 Mailpit HTTP API 发送邮件，邮件保留在 Mailpit 中
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

# 发送邮件
/scripts/mailpit.py

