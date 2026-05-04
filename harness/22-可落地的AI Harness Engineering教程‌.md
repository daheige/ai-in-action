AI Harness Engineering 是一套系统化的方法论与工具集，旨在让大语言模型（LLM）从“能说”进化为“能做”——通过构建结构化的执行环境（Harness），使 AI 能够调用工具、管理上下文、执行任务并持续迭代，最终完成端到端的复杂工作流。

以下是详细、可落地的 AI Harness Engineering 工具安装与配置教程，涵盖主流框架、本地部署方案及 `agent.md` 配置实践，帮助你从零搭建一个稳定可用的 AI Agent 系统。

---

一、核心工具选型与功能定位

| 工具/平台 | 类型 | 核心能力 | 适用场景 |
|----------|------|---------|--------|
| Ollama + GPT-OSS | 本地化 LLM 运行环境 | 完全离线、私有、零成本运行大模型 | 数据敏感、需隐私保护的开发测试 |
| Model Context Protocol (MCP) | 上下文与工具集成协议 | 统一接入浏览器、数据库、文件系统等外部资源 | 多工具协同、长期任务执行 |
| OpenClaw / Claude Code | Agent Harness 框架 | 提供完整的 Agent 循环、工具链和记忆系统 | 编程、自动化运维、内容生成 |
| Cursor | AI 编程 IDE | 内置 Plan 模式、Skills、Hooks，支持长任务迭代 | 代码编写、项目重构、测试修复 |
| Harness.io | CI/CD 平台（同名但不同域） | 自动化软件交付流程，AI 驱动部署 | 企业级 DevOps 流水线 |

> ⚠️ 注意：AI Agent Harness 与 Harness.io（CI/CD 平台） 名称相似但用途不同，本文聚焦前者。

---

二、本地 AI Harness Agent 安装与配置（基于 Ollama + GPT-OSS）

✅ 场景说明
适合希望在个人电脑上搭建完全离线、私有、可编程的 AI Agent 的开发者，无需依赖云端 API，避免数据外泄。

步骤 1：安装 Ollama（一键本地 LLM 运行时）

前往官网下载并安装：[Ollama](https://ollama.com)

```bash
macOS / Linux 安装命令
curl -fsSL https://ollama.com/install.sh | sh

启动服务
ollama serve
```

步骤 2：拉取 GPT-OSS 模型（推荐 20B 版本）

```bash
下载适合普通设备的版本
ollama pull gpt-oss:20b

若有高性能 GPU，可选更强版本
ollama pull gpt-oss:120b
```

步骤 3：创建 Agent 执行脚本 `agent_harness_local.py`

```python
import json
import subprocess
from openai import OpenAI

配置本地 Ollama 接口
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  任意值即可
)

MODEL = "gpt-oss:20b"

def initializer_setup(project_name: str, goal: str):
    workspace = f"./workspaces/{project_name}"
    subprocess.run(["mkdir", "-p", workspace])
    
    features = {
        "features": [
            {
                "category": "core",
                "description": goal,
                "steps": [],
                "passes": False
            }
        ]
    }
    
    with open(f"{workspace}/feature_list.json", "w") as f:
        json.dump(features, f, indent=2)
    
    with open(f"{workspace}/harness-progress.txt", "w") as f:
        f.write(f"项目启动: {goal}\n")
    
    subprocess.run(["git", "init"], cwd=workspace)
    print(f"✅ 项目 {project_name} 已初始化完成")
```

步骤 4：运行 Agent 并启动任务

```bash
python agent_harness_local.py
```

此时你已拥有一个具备项目初始化、文件操作、Git 管理能力的本地 AI Agent。



---

三、配置 `agent.md` —— AI Agent 的“操作手册”

`agent.md` 是 Anthropic 官方提出的标准配置文件，用于定义 AI Agent 的行为边界、技能、规则和权限。它是 Harness Engineering 中“Instructions”层的核心载体。

📄 示例：`agent.md` 文件模板

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

✅ 使用方式

将该文件作为上下文注入到 Agent 的提示词中，或通过 `--context-file agent.md` 参数传入主程序。



---

四、进阶配置：集成 MCP 与 Skills 系统

1. 安装 Model Context Protocol (MCP) 服务器

```bash
npm install -g @modelcontextprotocol/server
mcp-server --port 8080
```

2. 配置工具连接（如浏览器自动化）

在 `config.yaml` 中添加：

```yaml
tools:
  mcp_endpoints:
    - name: browser-use
      url: http://localhost:8080
      capabilities:
        - browse
        - screenshot
        - interact
```

3. 创建 Skill 文件 `skills/web_scraping.md`

```markdown
---
skill_id: web-scrape-table
version: '1.0'
description: 从网页中提取表格数据
input_schema:
  url: string
  selector: string  CSS 选择器
---

你是一个网页数据提取专家。

请使用 MCP 工具访问指定 URL，定位到 `selector` 对应的表格元素，将其转换为 JSON 格式返回。

示例输出：
[
  {"姓名": "张三", "年龄": "25"},
  {"姓名": "李四", "年龄": "30"}
]
```

Agent 在执行任务时可动态加载此 Skill，实现即插即用的功能扩展。

---

五、企业级部署建议

1. 权限隔离：为每个 Agent 分配独立的飞书/钉钉机器人身份，避免消息混淆 
2. Git 作为外部记忆：利用提交历史追踪 Agent 行为，便于审计与回滚 
3. Hooks 自动化：配置 `pre-commit` 或 `post-test` 钩子，实现自动测试与修复 
4. 可观测性监控：记录每一步工具调用、输出结果与耗时，用于调试与优化 

---

六、总结

搭建一个高效的 AI Harness Agent，关键在于：

- 模型是大脑，Harness 是身体：没有好的执行框架，再强的模型也无法完成实际任务 
- Instructions 定规则，Tools 给能力，Skills 提效率：三者协同才能构建可持续进化的 AI 工作流 
- 本地化 + 离线化 = 安全可控：Ollama + GPT-OSS 方案为个人开发者提供了零成本、高隐私的实践路径 

> 🔗 延伸学习资源：
> - [Harness Engineering 教程](https://blog.csdn.net/Python_cocola/article/details/158887357) 
> - [AI Agent 六层架构避坑指南](https://blog.csdn.net/Trb201013/article/details/157979137) 
> - [Cursor Plan 模式实战](https://blog.csdn.net/qq_44810930/article/details/157506417) 
