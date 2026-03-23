---
name: sirchmunk
description: 遇到关键词"搜索"、"全文搜索"、"检索"、"查找"时，从用户输入中提取搜索关键词以及搜索模式，构造JSON请求体，使用curl命令发送POST请求并返回相关信息
---

# 文件夹结构
若需要获取文件结构，使用`eza --tree --level=3 --sort=newest ./`命令获取当前目录下的文件结构，并返回结果。


# api配置
- api_url = "10.17.1.26"
- api_port = "8584"

# 参数定义
arguments:
  query:
    type: string
    description: "搜索查询内容"
  mode:
    type: string
    description: "搜索模式，默认为FAST,还支持DEEP,FILENAME_ONLY,根据用户情景选择合适的搜索模式"
    default: "FAST"
  dir:
    type: string
    description: "使用`basename $(pwd)`获取当前目录的名称（不含路径）" 

## 搜索模式说明
| 模式                 | 说明       | 适用场景                 | 速度    |
| ------------------ | -------- | -------------------- | ----- |
| **FAST**           | 快速模式（默认） | 只搜索文件名和基本元数据，不深入文件内容 | ⚡ 最快  |
| **DEEP**           | 深度模式     | 递归扫描目录，读取文件内容进行全文搜索  | 🐢 较慢 |
| **FILENAME\_ONLY** | 仅文件名     | 只匹配文件名，不做任何内容检索      | ⚡ 最快  |


# 使用变量执行 curl命令
```
curl -X POST "http://${api_url}:${api_port}/api/v1/search" \
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
