驾驭工程（Harness Engineering） 是一套让AI智能体（Agent）在受控环境中安全、可靠、高效完成复杂任务的系统化工程方法论，其核心不仅是“使用AI”，而是“如何驾驭AI”。它包含多个关键组成部分，共同构成一个完整的运行与治理体系。

---

# 一、四大核心支柱（根据OpenAI实践框架）

1. 上下文架构（Context Architecture）  
   设计智能体可访问和理解的信息环境，避免“上下文腐化”（Context Rot）或“上下文污染”（Context Pollution）。  
   - 动态更新的知识库  
   - 可观测性数据集成（如日志、监控）  
   - 精准的文档结构与检索机制  

2. 架构约束（Architectural Constraints）  
   通过技术手段强制执行系统规则，确保AI行为不越界。  
   - 自定义代码格式与接口规范  
   - 机械式不变量（Mechanical Invariants）：如通过linter/CI自动检查  
   - 工具调用权限控制  

3. 反馈循环（Feedback Loops）  
   建立自动化的验证与纠错机制，使系统能自我修正。  
   - 自动测试与回归验证  
   - PR审查中的智能提示  
   - 用户行为数据反哺模型优化  

4. 熵治理（Entropy Management）  
   持续清理AI生成内容带来的混乱，保持系统整洁。  
   - 定期重构AI生成代码  
   - 删除冗余文件与无效逻辑  
   - 维护“Agent Captain”角色负责流程治理

---

# 二、三大核心类别（OpenAI官方分类）

1. 上下文工程（Context Engineering）  
   管理智能体“看到什么”，包括文档、提示、状态信息等，是Harness的第一层基础。

2. 架构约束（Architectural Constraints）  
   定义“系统阻止什么”，如禁止直接修改主干分支、强制走CI流程等。

3. 生命周期管理（Lifecycle Management）  
   覆盖智能体从任务分配、执行、验证到合并的全流程控制，确保端到端可控。

---

# 三、核心动作：四个动词闭环

Harness Engineering 的运作可抽象为四个关键动作，形成持续改进闭环：

- Constrain（约束）：设定边界与规则  
- Inform（告知）：提供上下文与知识  
- Verify（验证）：自动检查输出正确性  
- Correct（纠正）：发现问题并修复  

> 这四个动作构成了人类与AI协作的新范式：人类掌舵，智能体执行（Humans steer, agents execute）。

---

# 四、与相关概念的关系

| 概念 | 关注点 | 与Harness Engineering的关系 |
|------|------|----------------------------|
| Prompt Engineering | “怎么措辞？” | 被包含于Harness中，仅是单次交互优化 |
| Context Engineering | “模型看到什么？” | 是Harness的子集，聚焦信息供给 |
| Harness Engineering | “系统防止、测量、修复什么？” | 包含以上两者，并扩展至全生命周期管理 |

---
