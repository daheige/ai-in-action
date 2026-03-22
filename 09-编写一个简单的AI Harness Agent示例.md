# AI Harness Agent 配置文档参考

1. 概述

AI Harness Engineering 是一套用于构建和管理 AI Agent 的工程化框架体系。它提供了标准化的工具集、配置规范以及运行环境，使得 AI Agent 能够在一个可控、可扩展且具备反馈机制的环境中稳定运行。

本文档详细介绍了 AI Harness Agent 的安装配置步骤、框架目录结构及其关键配置项示例，帮助开发者快速搭建并部署自己的 AI Agent 系统。

---

2. 安装与配置步骤

步骤一：准备基础环境

```bash
推荐使用 Python >= 3.9 版本
sudo apt update && sudo apt install python3 python3-pip git -y

或 macOS 用户可通过 Homebrew 安装:
brew install python@3.9 git
```

步骤二：克隆项目仓库

```bash
git clone https://github.com/example/ai-harness-agent.git
cd ai-harness-agent
```

> 注：此处假设你已拥有访问权限至私有仓库；公开可用模板建议替换为实际链接。

步骤三：创建虚拟环境并激活

```bash
python3 -m venv .venv
source .venv/bin/activate Windows 下使用 `.venv\Scripts\activate`
```

步骤四：安装依赖包

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

步骤五：配置系统参数

编辑 `config.yaml` 文件以适配本地或远程服务：

```yaml
model_provider: "openai"         LLM 提供商名称（如 anthropic / ollama）
api_key_env_var: "OPENAI_API_KEY"
default_model: "gpt-4-turbo"

tools:
  browser_use_enabled: true      是否启用浏览器自动化能力
  file_system_access: false       是否允许读取宿主机文件系统
  database_connection_string: ""  数据库连接字符串（留空表示禁用）

logging_level: INFO              日志级别 DEBUG/INFO/WARNING/ERROR
max_iterations_per_task: 10      单次任务最大迭代次数限制
feedback_loop_timeout_seconds: 60 反馈等待超时时长(单位:s)
```

步骤六：启动 Agent 运行实例

```bash
python main.py start-agent \
    --name my_first_agent \
    --task-description="分析给定文本的情感倾向" \
    --context-file context/sentiment_analysis_skill.md
```

---

3. 框架结构说明

整个 AI Harness Agent 项目的组织遵循模块化的理念，便于维护与拓展：

```
.
├── README.md                   ← 项目概述文档
├── config.yaml                 ← 全局配置文件
├── main.py                     ← 应用主入口点
├── agents/
│   ├── __init__.py             ← 初始化模块
│   └── base_agent.py           ← 抽象基类定义
├── tools/
│   ├── __init__.py
│   ├── skill_loader.py          ← 上下文技能加载器
│   ├── hook_manager.py          ← 触发钩子处理器
│   └── subagent_coordinator.py  ← 子代理调度中心
├── harness_engine/
│   ├── __init__.py
│   ├── core.py                  ← 引擎核心逻辑控制单元
│   └── feedback_validator.py    ← 输出校验与修正模块
└── utils/
    ├── logger_setup.py          ← 自定义日志记录器封装
    └── helpers.py               ← 辅助函数集合
```

各部分职责划分如下：

| 目录 | 功能 |
|------|------|
| `agents/` | 封装各类 Agent 类型的具体实现 |
| `tools/` | 内建工具插件，涵盖技能加载、Hook 触发等通用功能 |
| `harness_engine/` | 整体引擎控制器，负责协调各个组件之间的协作关系 |
| `utils/` | 杂项辅助方法 |

---

4. 示例配置详解

下面是一个典型的 Skill Markdown 文档 (`skills/sentiment_analysis_skill.md`) 内容样例：

```markdown
---
skill_id: sentiment-analysis-v1
version: '1.0'
description: Analyze the emotional tone of a given text passage.
author: Your Name Here
tags: ["nlp", "classification"]
input_schema:
  type: object
  properties:
    input_text:
      type: string
required_fields: ['input_text']
output_format: json_object_with_emotion_label_and_confidence_score
execution_mode: interactive_or_batch
timeout_seconds: 30
retry_attempts_on_failure: 2
security_permissions_needed: []
external_dependencies_required: []
supported_languages: en,zh-CN
---

You are an expert in natural language processing and emotion classification.

Your task is to analyze the provided piece of text for its dominant emotional tone from one of these categories:

- Positive
- Negative
- Neutral

Return your result as a JSON-formatted response with two keys:
{
  "emotion": "<category>",
  "confidence": <float between 0 and 1>
}
```

此文档可用于动态注入到 Agent 当前上下文中，从而赋予其情感识别的能力。

另一个重要的配置案例是 Hook 设置，在某些情况下我们希望每当某个事件被触发就自动执行一段预设的操作序列。比如每次新消息到达时都先做一次关键词过滤再交给后续流程处理：

```json
[
  {
    "event_type": "message_received",
    "filter_rules": [
      {"contains_keywords": ["urgent", "important"]},
      {"exclude_senders": ["spam_bot"]}
    ],
    "actions_to_execute": [
      {"type": "log_event"},
      {"type": "notify_user", "target_channel": "alerts"}
    ]
  }
]
```

以上规则可在 `hooks/on_message_received.json` 中保存并通过 Hook Manager 加载生效。

---

## 总结

通过上述指南您可以顺利完成 AI Harness Agent 的基本部署，并理解其内部工作机制。随着更多高级特性的逐步加入（例如多模态输入支持、分布式计算集群对接等），这套框架将持续演进成为支撑智能决策系统的坚实底座。欢迎持续关注社区更新获取最新进展！
