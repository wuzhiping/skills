---
name: planka
description: 当用户请求包含 `planka` 或需要处理 Planka 任务时，自动处理 Todos 列表中的任务。
---

# Planka Task Processor

## Board
http://kanban.feg.cn/

## Target Lists

| List | Description |
|-----|-------------|
| Todos | 待处理任务 |
| Doing | 处理中 |
| Bad | 失败任务 |
| Completed | 完成任务 |

其他的list不处理。

## Workflow

1. 获取 **Todos 列表中的所有 cards**
2. 逐个处理 card

处理逻辑：

- Step1: 将 card 移动到 **Doing**
- Step2: 检查 card 描述中是否包含 **邮箱**
- Step3:
  - 如果 **没有邮箱** → 移动到 **Bad**
  - 如果 **存在邮箱** → 移动到 **Completed**
- Step4: 继续处理下一个 card

直到 Todos 为空。

---

# Planka API

API Docs:
https://plankanban.github.io/planka/swagger-ui/

Base URL
http://kanban.feg.cn/api


---

# Authentication

Token 必须从 **环境变量**读取,使用api必须使用token认证

---

# API reference

## 1 Get board details

GET /boards/1701298620386509829

return board information, including lists, cards, and other related data.

