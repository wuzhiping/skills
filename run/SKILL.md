---
name: run
description: 当用户需要 **调用 API**，或用户请求中包含关键字 **`api`** 时，调用远程接口并返回结果。
---

# 触发条件

当满足以下任一条件时触发：

1. 用户明确要求 **调用 API**
2. 用户请求中包含关键字 **`api`**
3. 用户请求涉及 API 列表中的功能

---

# API 基本信息

- **接口地址**: `https://example.com/API/call`
- **请求方式**: `POST`
- **请求头**: `Content-Type: application/json`
- **请求体格式**:

```json
{
  "func": "<函数名>",
  "pkg": "<包名>",
  "token": "<认证令牌>",
  "args": "<JSON字符串>"
}
```

---

## Authentication

API 调用需要认证 token。

token **不写死在 Skill 中**，必须从环境变量读取：

API_TOKEN

Skill 在调用 API 时使用：

token = $API_TOKEN

---

# 重要规则

⚠️ **args 必须是 JSON 字符串，而不是 JSON 对象**

---

# 执行方式

调用 API 通过运行脚本：

```
uv run /scripts/api_client.py
```

如果系统没有安装 `uv`，需要先安装：

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

# 执行流程

1. 识别用户请求中的 API 调用需求
2. 根据 API 列表确定：

* `func`
* `pkg`
* `token`
* `args`

3. 构造请求 JSON

```json
{
  "func": "...",
  "pkg": "...",
  "token": "...",
  "args": "..."
}
```

4. 执行 API 调用

```
uv run /scripts/api_client.py
```

5. 获取 API 返回结果
6. 将结果 **原样返回给用户**

---

# 执行原则

调用 API 时必须遵循以下原则：

### 1. 立即执行

识别到 API 调用需求后立即执行，不需要额外确认。

### 2. 返回原始结果

API 调用完成后，必须直接返回原始响应。

### 3. 不自动重试

如果调用失败：

* 直接返回错误信息
* 不自动重试
* 不尝试其他方案

---

# API 列表

以下是当前支持的 API：

| API名称  | 说明        | 参数文档                    |
| ------ | --------- | ----------------------- |
| 加法测试   | 测试 API 调用 | references/add.md       |
| 人事知识库  | 查询 HR 数据  | references/personnel.md |
| 銷售會議簡報 | 销售会议资料    | references/sale.md      |
| 資安資料   | 信息安全资料    | references/zian.md      |

---

# API 参数说明

每个 API 的参数说明在对应文档中,调用 API 时必须参考对应文档构造 `args`。

---

# Best Practices

为了提高成功率：

1. 所有 API 参数必须定义在 `references/*.md`
2. args 必须严格 JSON string
3. Skill 只负责 **调用 API，不处理业务逻辑**
4. API 返回内容直接透传给用户
