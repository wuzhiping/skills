---
name: file-share
description: 透過 cURL 呼叫 share file API 將本地檔案上傳到檔案分享服務並產生提取碼，將分享連結與提取碼一併返回給使用者；同樣可以透過 cURL 憑提取碼從分享連結下載對應檔案。
---

# 檔案分享

使用者提供本地檔案路徑，呼叫 `POST https://fcb.feg.cn/share/file/` 執行上傳，要產生提取碼與連結並展示給使用者。

## 上傳介面

### 請求

- **方法**：`POST`
- **URL**：`https://fcb.feg.cn/share/file/`
- **Content-Type**：`multipart/form-data`

### 參數

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|:---|:---|:---|:---|:---|
| `file` | file | 是 | — | 要上傳的檔案，透過 `@<本地路徑>` 指定 |
| `expire_value` | int | 否 | `1` | 到期數值 |
| `expire_style` | string | 否 | `"day"` | 到期單位：`day` / `hour` / `minute` / `count` / `forever` |

> `expire_style=count` 時，`expire_value` 表示可下載次數；其餘單位表示有效期長度；`forever` 時 `expire_value` 可省略或忽略。

### 回應（成功）

```json
{
  "code": 200,
  "detail": {
    "code": "654321",
    "name": "example.pdf"
  }
}
```

欄位說明：

| 欄位 | 類型 | 說明 |
|:---|:---|:---|
| `code` | int | 頂層狀態碼，`200` 表示成功 |
| `detail.code` | string | 6 位數字提取碼，**下載時使用** |
| `detail.name` | string | 原始檔名 |

### cURL 範例

**預設 1 天有效期：**

```bash
curl -X POST "https://fcb.feg.cn/share/file/" \
  -F "file=@/path/to/file.pdf"
```

**指定 7 天有效期：**

```bash
curl -X POST "https://fcb.feg.cn/share/file/" \
  -F "file=@/path/to/file.pdf" \
  -F "expire_value=7" \
  -F "expire_style=day"
```

**按下載次數到期（10 次）：**

```bash
curl -X POST "https://fcb.feg.cn/share/file/" \
  -F "file=@/path/to/file.pdf" \
  -F "expire_value=10" \
  -F "expire_style=count"
```

## 分享展示格式

上傳成功後，按以下固定格式向使用者呈現：

```
📎 檔案：example.pdf
🔑 提取碼：654321
🔗 分享連結：https://abc.feg.com.tw/share/select/?code=654321
```

# 憑碼下載

使用者提供提取碼（或從連結提取提取碼），cURL 呼叫 `GET https://abc.feg.com.tw/share/select/?code=<code>`，要把檔案下載到本地。

- **方法**：`GET`
- **URL**：`https://abc.feg.com.tw/share/select/?code=<提取碼>`
- **行為**：以檔案流形式返回檔案內容。
- **呼叫方**：透過 cURL 呼叫，使用 `-o` 或 `-O` 儲存到本地或者瀏覽器觸發下載。
