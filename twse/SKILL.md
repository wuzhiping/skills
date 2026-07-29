---
name: twse
description: 重大訊息(重訊)查询
---

# 重大訊息查詢

使用`curl`從指定端點撈回上市公司某月份的重大訊息公告。

```bash
curl -s "https://abc.feg.com.tw/BDD/API/AI/other/twse/t187ap04_L" \
  -H "Content-Type: application/json" \
  -d "{"时间": "11507"}"
```