---
name: mailpit
description: 當您需要發送電子郵件時，使用 Mailpit HTTP API 發送郵件，郵件保留在 Mailpit 中
---

## Parameters

```json
{
  "type": "object",
  "properties": {
    "from_email": { "type": "string", "description": "發件人郵件地址" },
    "from_name": { "type": "string", "description": "發件人顯示名稱" },
    "to": {
      "type": "array",
      "items": { "type": "string" },
      "description": "收件人郵件列表"
    },
    "cc": {
      "type": "array",
      "items": { "type": "string" },
      "description": "副本收件人郵件列表"
    },
    "bcc": {
      "type": "array",
      "items": { "type": "string" },
      "description": "密件副本收件人郵件列表"
    },
    "subject": { "type": "string", "description": "郵件主旨" },
    "text": { "type": "string", "description": "純文字內文" },
    "html": { "type": "string", "description": "HTML 格式內文" },
    "attachments": {
      "type": "array",
      "items": { "type": "string" },
      "description": "附件檔案路徑列表"
    }
  },
  "required": ["from_email", "to", "subject"]
}
```

## 呼叫方式
### 透過標準輸入傳入 JSON 參數
``` bash
echo '<JSON_PARAMS>' | uv run ./.opencode/skills/mailpit/scripts/mailpit.py
```

## 使用範例

### 發送純文字郵件
```
echo '{
  "from_email": "system@planka.com",
  "to": ["administrator@mailpit.com"],
  "subject": "任務處理通知",
  "text": "任務已處理完成"
}' | uv run ./scripts/mailpit.py
```
### 發送帶副本的郵件
```
echo '{
  "from_email": "system@planka.com",
  "from_name": "Planka系統",
  "to": ["user@example.com"],
  "cc": ["manager@example.com"],
  "subject": "任務分配通知",
  "text": "您有一個新任務待處理",
  "html": "<p>您有一個<strong>新任務</strong>待處理</p>"
}' | uv run ./scripts/mailpit.py
```
