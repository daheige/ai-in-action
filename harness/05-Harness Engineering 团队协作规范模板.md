Harness Engineering 团队协作规范模板

1. 角色定义与职责分工
> 明确人与AI Agent的协作边界，构建“指挥官-执行者-监督者”三位一体的工程角色体系。

| 角色 | 职责 | 权限范围 | 工具支持 |
|------|------|----------|----------|
| 项目指挥官（Human） | 定义业务目标、审批任务优先级、仲裁冲突 | 拥有最终合并权、可修改全局AGENTS.md | Jira / 飞书多维表格 |
| 架构师 Agent | 拆解需求、设计技术方案、定义接口契约 | 可读取 `/docs/specs`，生成 `API.md` | OpenClaw + MCP 工具集 |
| 开发 Agent | 实现功能代码，遵循约束规则 | 仅限访问 `/src/features/{module}`，禁止跨目录修改 | GitWorktree + Linter + Docker沙箱 |
| 测试 Agent | 执行单元/集成/UI测试，验证验收标准 | 可调用Puppeteer MCP、Selenium、Postman | CI/CD流水线 + Chrome DevTools协议 |
| 文档 Agent | 生成/更新技术文档、API说明、使用手册 | 自动同步至 `/docs/`，触发版本标记 | Doc Gardening Agent + MkDocs |
| 审查 Agent | 静态分析、安全扫描、代码风格校验 | 执行SAST、DAST、ESLint、Bandit | GitHub Code Scanning / SonarQube |

> ✅ 协作原则：所有Agent不得直接修改主分支，所有变更必须通过PR提交，由审查Agent自动评分，低于85分禁止合并。

---

2. 任务调度与并行机制
> 采用“线性流水线 + 依赖图并行”双模式，适配不同复杂度任务。

| 模式 | 适用场景 | 流程说明 | 协作示例 |
|------|----------|----------|----------|
| 线性流水线 | 标准功能开发（如登录页） | 需求 → 架构设计 → 编码 → 测试 → 文档 → 审查 → 合并 | 架构师生成接口规范 → 开发Agent写代码 → 测试Agent跑用例 → 文档Agent写README → 审查Agent打分 |
| 依赖图并行 | 大型模块开发（如支付系统） | 多子任务并行执行，依赖关系由主Agent动态构建 | 支付网关开发与风控规则开发并行 → 集成测试阶段合并 → 自动触发端到端验证 |

> 🔄 冲突解决机制：  
> - 若多个Agent修改同一文件，系统自动检测并触发“合并仲裁”流程  
> - 由审查 Agent 比对变更差异，生成冲突报告并建议最优合并方案  
> - 人工指挥官仅在仲裁失败时介入

---

3. 上下文管理规范
> 所有AI行为必须基于结构化、版本化、可追溯的上下文。

- 项目级上下文：`AGENTS.md`（根目录）  
  - 包含：项目目标、架构图、技术栈、安全策略、变更流程
- 模块级上下文：`src/auth/AGENTS.md`  
  - 包含：接口定义、依赖关系、历史变更记录、失败案例库
- 任务级上下文：`/tasks/login/TASK.md`  
  - 包含：用户故事、验收标准、预期响应时间、测试用例编号

> 📌 强制要求：  
> - 所有Agent必须在执行前读取对应层级的 `AGENTS.md`  
> - 文档变更必须通过PR提交，由文档 Agent 自动同步至所有工作区  
> - 禁止使用非结构化文档（如Word、PDF）作为唯一依据

---

4. 验证与反馈闭环
> 所有AI输出必须通过自动化质量门禁，失败即回滚。

| 验证层级 | 检查项 | 工具 | 阈值 |
|----------|--------|------|------|
| 代码质量 | ESLint / Prettier | GitHub Actions | 0 错误 |
| 安全合规 | SAST扫描（Semgrep、Trivy） | GitLab CI | 无高危CVE |
| 功能正确 | 单元测试覆盖率 | Jest / PyTest | ≥90% |
| 接口兼容 | OpenAPI Schema校验 | Spectral | 无破坏性变更 |
| UI体验 | Puppeteer截图比对 | Chrome DevTools协议 | 布局偏差 ≤1px |
| 性能指标 | 响应时间、启动耗时 | Locust / JMeter | ≤500ms |

> 🚨 失败处理流程：  
> CI失败 → 自动将错误日志注入Agent上下文 → Agent重试 → 重试失败3次 → 触发“人工介入”工单 → 指挥官评估是否调整约束规则

---

5. 持续进化机制
> 系统应具备“错误即学习”的自我修复能力。

- 错误模式库：  
  - 每次CI失败自动生成一条“防错规则”（如：“空指针异常 → 自动添加判空”）  
  - 存储于 `/rules/failure-patterns.json`，由审查 Agent 定期合并至Linter规则集
- 文档园艺：  
  - 文档 Agent 每周扫描 `AGENTS.md` 与代码差异，标记过时内容  
  - 自动创建“文档更新”PR，由指挥官审批
- 权限审计：  
  - 每月生成《Agent行为报告》：  
    - 越界操作次数  
    - 重复错误类型  
    - 任务完成效率  
  - 用于优化角色分工与约束策略

---

6. 工具链推荐（团队适配）
| 功能 | 推荐工具 | 说明 |
|------|----------|------|
| 代码托管 | GitHub / Gitee | 支持PR流程、Code Scanning、Actions |
| CI/CD | Jenkins / GitHub Actions | 集成AI检查点，支持自定义脚本 |
| Agent框架 | OpenClaw或其他agent框架 | 支持本地部署、百炼API接入、飞书通知 |
| 上下文管理 | Notion / 飞书多维表格 | 结构化存储AGENTS.md、TASK.md |
| 协作沟通 | 飞书/dingding/slack/企业微信 | 与OpenClaw深度集成，自动推送任务状态 |
| 监控告警 | Prometheus + Grafana | 监控Agent任务成功率、平均耗时 |

---


> 💡 落地建议：  
> 从一个单任务（如“自动生成API文档”）开始，使用上述模板配置3个Agent（架构师+开发+审查），运行2周后评估效率提升与错误率下降，再逐步扩展至完整团队。  
> 团队可优先接入飞书/dingding/slack/企业微信+OpenClaw，实现“需求在飞书/dingding/slack等平台输入，代码自动交付”的无缝协
