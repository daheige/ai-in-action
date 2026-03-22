Anthropic 官方标准配置文件 `agent.md` 格式详解

Anthropic 提出的 `agent.md` 格式是一种标准化的配置文件，用于定义 AI Agent 的行为、技能和上下文。这种格式支持跨平台兼容，使得 Agent 能够在不同工具（如 Claude Code、Cursor、GitHub Copilot 等）中保持一致的行为。

格式结构

`agent.md` 文件采用 YAML 前言（frontmatter）与 Markdown 内容相结合的结构：

```markdown
---
agent_id: dev-agent-v1
version: '1.0'
name: Local Development Agent
description: A private, offline AI assistant for coding, debugging, and project management.
author: You
tags: [coding, automation, local]
llm_model: gpt-oss:20b
max_iterations: 10
timeout_seconds: 300
---

🎯 目标与边界

- 任务目标：根据用户需求自动创建项目、编写代码、运行测试、修复错误直至通过。
- 禁止行为：
  - 不得修改 `/system` 或 `/root` 目录
  - 不得执行 `rm -rf /` 等危险命令
  - 不得访问网络请求（离线模式）

🔧 工具权限

- ✅ 允许：读写 `./workspaces/` 目录、执行 Bash 命令、调用 Git
- ❌ 禁止：网络请求、数据库连接、系统级更改

🧠 技能列表（Skills）

1. 项目初始化
- 触发条件：用户输入“新建项目”
- 动作流程：
  1. 创建项目目录
  2. 初始化 Git
  3. 生成 `README.md` 和基础结构

2. 单元测试生成
- 输入：Python 文件路径
- 输出：同目录下 `_test.py` 文件
- 使用框架：`pytest`

🔄 反馈机制

- 每次代码生成后自动运行 `pytest`
- 若失败，分析错误日志并尝试修复，最多重试 3 次
- 超过限制则暂停并通知用户介入

📁 上下文管理

- 所有项目保存在 `./workspaces/{project_name}`
- 使用 `harness-progress.txt` 记录执行状态
- 利用 Git 提交历史作为外部记忆
```

agent.md文档核心字段说明：

1. YAML 前言字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `agent_id` | string | Agent 唯一标识符 |
| `version` | string | 版本号 |
| `name` | string | Agent 名称 |
| `description` | string | Agent 功能描述 |
| `author` | string | 创建者 |
| `tags` | array | 标签列表，用于分类 |
| `llm_model` | string | 指定使用的 LLM 模型 |
| `max_iterations` | number | 最大迭代次数 |
| `timeout_seconds` | number | 超时时间（秒） |

2. Markdown 内容部分

内容部分用于详细描述 Agent 的行为规则、技能、权限和上下文管理方式。建议采用以下结构：

1. 目标与边界：明确 Agent 的任务目标和行为限制
2. 工具权限：定义 Agent 可访问的资源和工具
3. 技能列表：列出 Agent 的核心技能及其触发条件
4. 反馈机制：描述 Agent 如何处理错误和迭代
5. 上下文管理：说明如何处理和存储上下文信息

## 一个实际应用agent.md文档示例

一个典型的 `agent.md` 文件示例如下：

```markdown
---
agent_id: web-scraping-agent
version: '1.0'
name: Web Scraping Agent
description: An agent specialized in extracting structured data from websites
author: AI Engineer
tags: [web-scraping, data-extraction, automation]
llm_model: claude-3-5-sonnet-20241022
max_iterations: 5
timeout_seconds: 600
---

🎯 任务目标

- 从指定网页提取结构化数据
- 将数据转换为 JSON 格式
- 处理反爬虫机制和动态内容

🔧 工具权限

- ✅ 允许：访问网络、解析 HTML、执行 JavaScript
- ❌ 禁止：修改本地文件、访问数据库、执行系统命令

🧠 技能列表

1. HTML 解析
- 触发条件：用户输入包含 HTML 内容的 URL
- 动作流程：
  1. 请求网页内容
  2. 解析 HTML 结构
  3. 提取所需数据

2. 数据格式化
- 输入：原始数据
- 输出：JSON 格式数据
- 转换规则：保持字段一致性，处理缺失值

🔄 反馈机制

- 每次数据提取后验证结构完整性
- 若数据格式不正确，尝试使用备用解析策略
- 超过最大迭代次数则返回错误信息

📁 上下文管理

- 使用临时目录存储中间结果
- 记录请求历史和错误日志
- 清理临时文件避免资源占用
```

这种格式确保了 Agent 在不同平台和工具中的一致性，同时提供了清晰的配置和行为定义。
