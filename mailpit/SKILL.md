---
name: mailpit
description: 当您需要发送电子邮件时，使用 Mailpit HTTP API 发送邮件，邮件保留在 Mailpit 中
---

## Parameters

```json
{
  "type": "object",
  "properties": {
    "from_email": { "type": "string", "description": "发件人邮箱地址" },
    "from_name": { "type": "string", "description": "发件人显示名称" },
    "to": {
      "type": "array",
      "items": { "type": "string" },
      "description": "收件人邮箱列表"
    },
    "cc": {
      "type": "array",
      "items": { "type": "string" },
      "description": "抄送人邮箱列表"
    },
    "bcc": {
      "type": "array",
      "items": { "type": "string" },
      "description": "密送人邮箱列表"
    },
    "subject": { "type": "string", "description": "邮件主题" },
    "text": { "type": "string", "description": "纯文本正文" },
    "html": { "type": "string", "description": "HTML格式正文" },
    "attachments": {
      "type": "array",
      "items": { "type": "string" },
      "description": "附件文件路径列表"
    }
  },
  "required": ["from_email", "to", "subject"]
}
```

## 调用方式
### 通过标准输入传入 JSON 参数
``` bash
echo '<JSON_PARAMS>' | uv run ./.opencode/skills/mailpit/scripts/mailpit.py
```

## 使用示例

### 发送纯文本邮件
```
echo '{
  "from_email": "system@planka.com",
  "to": ["administrator@mailpit.com"],
  "subject": "任务处理通知",
  "text": "任务已处理完成"
}' | uv run ./scripts/mailpit.py
```
### 发送带抄送的邮件
```
echo '{
  "from_email": "system@planka.com",
  "from_name": "Planka系统",
  "to": ["user@example.com"],
  "cc": ["manager@example.com"],
  "subject": "任务分配通知",
  "text": "您有一个新任务待处理",
  "html": "<p>您有一个<strong>新任务</strong>待处理</p>"
}' | uv run ./scripts/mailpit.py
```
