---
name: run
description: 用户需要调用api，或用户请求中包含`api`时，根据用户的请求，运行指定的api，并返回结果
---

# 基本信息

- **地址**：`https://abc.feg.com.tw/BDD/API/AI/chatBot/ntfy/coder_run`
- **请求方式**：POST
- **请求头**：`Content-Type: application/json`
- **请求格式**：
```json
{
  "func": "<函数名>",
  "pkg": "<包名>",
  "token": "<认证令牌>",
  "args": "<JSON字符串>"
}
```

## 核心机制

- 通过 `func` + `pkg` + `token` + `args` 四参数调用指定功能。
- 调用/scripts/api_client.py中的`call_coder_run`函数，传入上述四个参数，即可完成调用。

**关键规则**：`args` 必须是 **JSON 字符串**，而非 JSON 对象。

**执行原则**：

1. **立即执行**：识别到触发条件后，直接构造请求调用 API
2. **无论成败**：调用后立刻将原始结果返回给用户
3. **不做加工**：不解释、不转换、不补充说明，原样返回 API 响应
4. **不重试**：失败时直接返回错误信息，不自动重试或换方案


## api List

- **加法测试**: 请参阅 [add.md](references/add.md) 获取参数详情
- **人事知识库**: 请参阅 [personnel.md](references/personnel.md) 获取参数详情
- **銷售會議簡報**: 请参阅 [sale.md](references/sale.md) 获取参数详情
- **資安資料**: 请参阅 [zian.md](references/zian.md) 获取参数详情


