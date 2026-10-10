---
name: sirchmunk
description: 遇到關鍵字「搜尋」、「全文搜尋」、「檢索」、「查找」時，從使用者輸入中擷取搜尋關鍵字以及搜尋模式，構造 JSON 請求體，使用 curl 命令發送 POST 請求並返回相關資訊
---

# 資料夾結構
若需要取得檔案結構，使用`eza --tree --level=3 --sort=newest ./`命令取得當前目錄下的檔案結構，並返回結果。

# 參數定義
arguments:
  query:
    type: string
    description: "搜尋查詢內容"
  mode:
    type: string
    description: "搜尋模式，預設為 FAST，還支援 DEEP、FILENAME_ONLY，根據使用者情景選擇合適的搜尋模式"
    default: "FAST"
  dir:
    type: string
    description: "使用`basename $(pwd)`取得當前目錄的名稱（不含路徑）" 

## 搜尋模式說明
| 模式                 | 說明       | 適用場景                 | 速度    |
| ------------------ | -------- | -------------------- | ----- |
| **FAST**           | 快速模式（預設） | 只搜尋檔名和基本中繼資料，不深入檔案內容 | ⚡ 最快  |
| **DEEP**           | 深度模式     | 遞迴掃描目錄，讀取檔案內容進行全文搜尋  | 🐢 較慢 |
| **FILENAME\_ONLY** | 僅檔名     | 只匹配檔名，不做任何內容檢索      | ⚡ 最快  |


# 使用變數執行 curl 命令
```
curl -X POST " https://sirch.feg.cn/api/v1/search" \
 -H 'accept: application/json'\
 -H 'content-type: application/json' \
 -d '{
    "query": "${arguments.query}",
    "paths": ["/mnt/${arguments.dir}"],
    "mode": "${arguments.mode}",           
    "enable_dir_scan": True, 
    "max_depth": 5,           
    "top_k_files": 3,         
    "max_token_budget": 8192,
  }'
```
