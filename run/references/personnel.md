
---

# API: personnel

## Description

查询公司人事知识库信息。

---

## API Mapping

func: ragflow  
pkg: tools

---

## Args Schema

args 必须是 JSON 字符串，结构如下：

```json
{
  "kb_ids": ["54558750c91311f08df50242ac1c0005"],
  "question": string
}