---
name: file-share
description: 使用 cURL `share file`,实现文件上传,并生成提取码,返回链接给用户
---

## 流程

### 1. 文件上传

**POST** `/share/file/`

**Content-Type:** `multipart/form-data`

#### 请求参数：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|:---|:---|:---|:---|:---|
| `file` | file | 是 | - | 要上传的文件 |
| `expire_value` | int | 否 | `1` | 过期数值 |
| `expire_style` | string | 否 | `"day"` | 过期时间单位：`day`/`hour`/`minute`/`count`/`forever` |

#### 响应示例

```json
{
  "code": 200,
  "detail": {
    "code": "654321",
    "name": "example.pdf"
  }
}
```

#### cURL 示例：

# 上传文件（默认1天有效期）
curl -X POST "http://fcb.feg.cn/share/file/" \
  -F "file=@/path/to/file.pdf"

# 上传文件并指定有效期（7天）
curl -X POST "http://fcb.feg.cn/share/file/" \
  -F "file=@/path/to/file.pdf" \
  -F "expire_value=7" \
  -F "expire_style=day"

# 上传文件并指定有效期（可下载10次）
curl -X POST "http://fcb.feg.cn/share/file/" \
  -F "file=@/path/to/file.pdf" \
  -F "expire_value=10" \
  -F "expire_style=count"

## 2. 文件分享

### 展示给用户示例：
- 文件：example.pdf
- 提取码：654321
- 点击即可保存文件： https://abc.feg.com.tw/share/select/?code=654321
