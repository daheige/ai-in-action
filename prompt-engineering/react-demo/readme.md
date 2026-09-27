# react 示例
ReAct 框架允许 LLMs 与外部工具交互来获取额外信息，从而给出更可靠和实际的回应。

## uv 安装虚拟环境
```shell
uv venv
source .venv/bin/activate
```

## uv 安装依赖
```shell
uv pip install requests
uv pip install dotenv
uv pip install openai
```
或者执行运行如下命令：从 requirements.txt 安装依赖
```shell
uv pip install -r requirements.txt
```

## 运行程序
```shell
python react-demo.py
```

python react-demo.py

运行结果如下：

我需要先了解Rust语言的基本信息，然后搜索它在AI领域的发展趋势和未来5年的预测。
Action: Search
Action Input: Rust语言是什么 特点 优势
看起来搜索工具没有返回结果。让我换个方式再试一次。

Action: Search
Action Input: Rust programming language introduction features
看起来搜索工具暂时不可用。不过我可以基于自己的知识来回答这个问题。

Question: rust语言是什么？它未来发展趋势，特别是ai领域，未来5年发展怎么样?

Thought: 搜索工具没有返回结果，但我对Rust语言及其在AI领域的发展有足够的了解，可以直接回答。

Final Answer:

## Rust语言是什么？

Rust是一种由Mozilla主导开发的系统级编程语言，2010年首次发布，2015年发布1.0稳定版。它的核心特点包括：

1. **内存安全**：通过所有权（Ownership）、借用（Borrowing）和生命周期（Lifetime）机制，在编译期就消除空指针、悬垂指针和数据竞争等内存安全问题，无需垃圾回收器（GC）。
2. **零成本抽象**：高级抽象不会带来运行时性能损失，性能可与C/C++媲美。
3. **并发安全**：编译器强制保证线程安全，让"无畏并发"成为可能。
4. **现代工具链**：Cargo包管理器、rustfmt、clippy等工具非常完善。
5. **强类型系统**：模式匹配、trait系统、枚举等特性强大。

Rust连续多年被Stack Overflow评为"最受开发者喜爱的编程语言"。

## 未来发展趋势

**整体趋势：**
- 已被Linux内核、Windows、Android等主流系统采纳
- 2024年Rust进入Linux内核6.1+，微软、Google、AWS等大厂持续投入
- 在WebAssembly、嵌入式、区块链、云原生（如Firecracker）领域增长迅速
- 被美国NSA、白宫等机构推荐为内存安全语言

## AI领域未来5年发展（2025-2030）

**乐观因素：**
1. **性能需求**：AI推理引擎、边缘AI对低延迟、低内存占用要求高，Rust优势明显。已有项目如`burn`、`candle`（Hugging Face）、`tch-rs`等。
2. **基础设施层**：AI框架底层、推理运行时（如ONNX Runtime部分组件）、向量数据库（如Qdrant、LanceDB）大量采用Rust。
3. **安全关键AI**：自动驾驶、机器人、医疗AI等对内存安全要求高的场景，Rust是理想选择。
4. **大厂推动**：Hugging Face、AWS（Bedrock部分组件）、微软等持续投入Rust AI生态。

**挑战与限制：**
1. **生态成熟度**：相比Python（PyTorch/TensorFlow），Rust的AI生态仍不成熟，学习曲线陡峭。
2. **研究友好性**：AI研究迭代快，Python的动态性和丰富库仍是主流，Rust更适合"部署"而非"研究"。
3. **人才储备**：Rust AI工程师相对稀缺。
4. **GPU生态**：CUDA绑定、分布式训练等仍不如Python完善。

**5年预测：**
- Rust不会取代Python成为AI研究主流语言
- 但在**AI推理、边缘部署、AI基础设施、高性能算子**领域份额会显著提升
- 可能出现1-2个有影响力的Rust原生AI框架
- "Python训练 + Rust部署"的混合模式会成为常见范式
- 在AI安全、自动驾驶、机器人等垂直领域，Rust采用率会快速增长

**总结**：Rust在AI领域未来5年将从"小众选择"走向"重要补充"，尤其在性能和安全性关键的部署环节，但短期内难以撼动Python在研究领域的主导地位。

最终答案: ## Rust语言是什么？

Rust是一种由Mozilla主导开发的系统级编程语言，2010年首次发布，2015年发布1.0稳定版。它的核心特点包括：

1. **内存安全**：通过所有权（Ownership）、借用（Borrowing）和生命周期（Lifetime）机制，在编译期就消除空指针、悬垂指针和数据竞争等内存安全问题，无需垃圾回收器（GC）。
2. **零成本抽象**：高级抽象不会带来运行时性能损失，性能可与C/C++媲美。
3. **并发安全**：编译器强制保证线程安全，让"无畏并发"成为可能。
4. **现代工具链**：Cargo包管理器、rustfmt、clippy等工具非常完善。
5. **强类型系统**：模式匹配、trait系统、枚举等特性强大。

Rust连续多年被Stack Overflow评为"最受开发者喜爱的编程语言"。

## 未来发展趋势

**整体趋势：**
- 已被Linux内核、Windows、Android等主流系统采纳
- 2024年Rust进入Linux内核6.1+，微软、Google、AWS等大厂持续投入
- 在WebAssembly、嵌入式、区块链、云原生（如Firecracker）领域增长迅速
- 被美国NSA、白宫等机构推荐为内存安全语言

## AI领域未来5年发展（2025-2030）

**乐观因素：**
1. **性能需求**：AI推理引擎、边缘AI对低延迟、低内存占用要求高，Rust优势明显。已有项目如`burn`、`candle`（Hugging Face）、`tch-rs`等。
2. **基础设施层**：AI框架底层、推理运行时（如ONNX Runtime部分组件）、向量数据库（如Qdrant、LanceDB）大量采用Rust。
3. **安全关键AI**：自动驾驶、机器人、医疗AI等对内存安全要求高的场景，Rust是理想选择。
4. **大厂推动**：Hugging Face、AWS（Bedrock部分组件）、微软等持续投入Rust AI生态。

**挑战与限制：**
1. **生态成熟度**：相比Python（PyTorch/TensorFlow），Rust的AI生态仍不成熟，学习曲线陡峭。
2. **研究友好性**：AI研究迭代快，Python的动态性和丰富库仍是主流，Rust更适合"部署"而非"研究"。
3. **人才储备**：Rust AI工程师相对稀缺。
4. **GPU生态**：CUDA绑定、分布式训练等仍不如Python完善。

**5年预测：**
- Rust不会取代Python成为AI研究主流语言
- 但在**AI推理、边缘部署、AI基础设施、高性能算子**领域份额会显著提升
- 可能出现1-2个有影响力的Rust原生AI框架
- "Python训练 + Rust部署"的混合模式会成为常见范式
- 在AI安全、自动驾驶、机器人等垂直领域，Rust采用率会快速增长

**总结**：Rust在AI领域未来5年将从"小众选择"走向"重要补充"，尤其在性能和安全性关键的部署环节，但短期内难以撼动Python在研究领域的主导地位。