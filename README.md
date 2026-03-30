# 5 Agent Skill design patterns every ADK developer should know
[5 Agent Skill design patterns](https://x.com/GoogleCloudTech/article/2033953579824758855)

# links
* [autoresearch](https://github.com/karpathy/autoresearch)
* [autoresearch-skill](https://skills.sh/olelehmann100kmrr/autoresearch-skill/autoresearch)
* [qmd](https://github.com/tobi/qmd)
* [openviking](https://skills.sh/volcengine/openviking/openviking)
* [opencli](https://opencli.info/docs/zh/)
* [Skill Seekers](https://skillseekersweb.com/zh/)
  
# AI 技能与 RAG
[sirchmunk](https://modelscope.github.io/sirchmunk-web/zh/) Raw Data to Self-Evolving Intelligence
```
docker run -d -it \
          --name sirchmunk \
          --cpus="4" \
          --memory="2g" \
          -p 8584:8584 \
          -e LLM_API_KEY="sk-abc" \
          -e LLM_BASE_URL="http://litellm.feg.cn/v1" \
          -e LLM_MODEL_NAME="ministral-3" \
          -e LLM_TIMEOUT=60.0 \
          -e UI_THEME=light \
          -e UI_LANGUAGE=zh \
          -e SIRCHMUNK_VERBOSE=true \
          -e SIRCHMUNK_ENABLE_CLUSTER_REUSE=true \
          -e SIRCHMUNK_SEARCH_PATHS=/mnt/docs \
          -v $PWD/data:/data/sirchmunk \
          -v /home/shawoo/cogs/abc/static/md:/mnt/docs:ro \
          modelscope-registry.cn-beijing.cr.aliyuncs.com/modelscope-repo/sirchmunk:ubuntu22.04-py312-0.0.6

```

# 📋Skills evaluated
[The Open Agent Skills Ecosystem](https://skills.sh/)

## 🏁gene
* Skill 是“做什么”，Gene 是“如何做”。
* Skill 关注任务，Gene 关注方法。
---
[https://evomap.ai/]
* 模型层解决“能不能思考”
* 工具层解决“能不能行动”
* Skill 层解决“能不能完成任务”
* 那 EvoMap 试图解决的是： “能力如何在群体中持续进化？”
---
它引入的核心思想来自生物学：
* 经验可以被封装为“基因”
* 基因可以被继承
* 不同基因可以重组
* 优质表达被强化
* 低效表达被淘汰
---
https://github.com/inclusionAI/AReaL/tree/main/examples/openclaw

## ☐obsidian-cli
* https://github.com/kepano/obsidian-skills
* https://github.com/vrtmrz/obsidian-livesync

## ☐browser-use-cli
https://docs.browser-use.com/open-source/browser-use-cli#browser-use-cli

## ✅self-improvement
https://skills.sh/pskoett/self-improving-agent/self-improvement

## ☐DCP
[https://github.com/Opencode-DCP/opencode-dynamic-context-pruning] Automatically reduces token usage in OpenCode by removing obsolete content from conversation history.

## ✅find-skills
【https://skills.sh/vercel-labs/skills/find-skills】 This skill helps you discover and install skills from the open agent skills ecosystem.

## ✅superpowers
[https://github.com/obra/superpowers] a complete software development workflow for your coding agents, built on top of a set of composable "skills" and some initial instructions that make sure your agent uses them.

## ☐AutoSkill
[[Pigs](https://github.com/wuzhiping/pig)](https://github.com/ECNU-ICALK/AutoSkill)

## ✅skill-writer
[https://skills.sh/pytorch/pytorch/skill-writer]
This Skill helps you create well-structured Agent Skills for Claude Code that follow best practices and validation requirements.

## ☐wiki-sop
JA SOP with media-wiki

## ☐[MemoryOS](https://github.com/BAI-LAB/MemoryOS)
[https://www.arscontexta.org/] memory infrastructure
* skills-graph

## ☐cron-jobs
submit pkflow jobs then trace process and result

## ☐coding-agent
Use bash (with optional background mode) for all coding agent work. Simple and effective.
etc. goose https://block.github.io/goose/docs/quickstart/

## ✅run
run OR async run a functional api throuth api gateway piper with credential token

## ✅fess
Enhanced web and package repository search using [FEG Enterprise Search Server] with SearXNG instance

## ✅web-fetch
[https://skills.sh/0xbigboss/claude-code/web-fetch] Fetch web content

[https://skills.sh/vaayne/agent-kit/web-fetch] Fetch web content, uv run scripts/web_fetch.py 🎉

## ✅planka
A elegant, open-source Kanban-style project management tool designed for real-time team collaboration,
follows the classic Kanban methodology

## ✅mailpit
Mailpit's SMTP relay (also called "message release") allows you to forward captured emails to a real SMTP server for actual delivery. 
This is useful when you want to selectively send emails to real recipients after inspecting them in the Mailpit web UI, or automatically relay specific messages.

## ☐dvc
[https://dvc.org/]

## ✅infographic
[https://infographic.antv.vision](https://github.com/antvis/Infographic/tree/main/skills)

## ✅sirchmunk
curl调用sirchmunk api搜索数据

---

# 📋Plugins
## ralph-loop
https://github.com/charfeng1/opencode-ralph-loop

## oh-my-opencode
https://ohmyopencode.org

https://www.opencode.asia/zh-cn/ecosystem/oh-my-opencode/

---

| 阶段                   | Emoji    | 说明      |
| -------------------- | -------- | ------- |
| **Todo / 待办**        | 📝 ☐     | 待处理、未开始 |
| **Plan / 计划**        | 📋 🗓️   | 已规划、排期中 |
| **Developing / 开发中** | 🚧 ⚙️ 🔨 | 进行中、构建中 |
| **QA / 测试**          | 🔍 🧪 ✅  | 审查中、测试中 |
| **Complete / 完成**    | ✓ 🎉 🏁  | 已完成、交付  |

---

**推荐组合（风格统一）：**

📝 **待办** → 📋 **计划** → 🚧 **开发** → 🔍 **测试** → ✅ **完成**

或更简洁的：

☐ **Todo** → 🗓️ **Plan** → ⚙️ **Dev** → 🧪 **QA** → ✓ **Done**
