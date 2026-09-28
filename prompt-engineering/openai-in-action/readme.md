# prompt 实战
基于 openai 风格，进行提示词工程实践

通过 OpenAI API，你可以使用大型语言模型根据提示生成文本，就像使用 ChatGPT 一样。这些模型几乎可以生成任何类型的文本回复，例如代码、数学公式、结构化的 JSON 数据，或类似人类的散文。

# 创建python虚拟环境
```shell
uv venv
source .venv/bin/activate
# 安装依赖
uv pip install openai

uv pip freeze >> requirements.txt
```

如果想本地开发，调试，查看openai相关信息，可以通过pip3安装openai
```shell
pip3 install openai --break-system-packages
```

# 运行程序
```shell
python simple-prompt.py
```
模型生成的内容数组位于响应的输出属性中。在这个简单示例中，我们只有一个输出，如下所示：
```json
[
  {
    "id": "msg_67b73f697ba4819183a15cc17d011509",
    "type": "message",
    "role": "assistant",
    "content": [
      {
        "type": "output_text",
        "text": "xxxxxx",
        "annotations": []
      }
    ]
  }
]
```

模型生成的内容数组位于响应的 output 属性中。在这个简单示例中，我们只有一个输出，看起来像这样：输出数组通常包含多个项目！它可能包含工具调用、推理模型生成的推理令牌数据以及其他内容。不能假设模型的文本输出一定位于 output[0].content[0].text。

通过API生成内容时，一个关键的选择是选择使用哪种模型——即上述代码示例中的模型参数。您可在此处查看所有可用模型的完整列表。在选择文本生成模型时，以下是一些需要考虑的因素。

推理型模型会生成内部思维链来分析输入提示，擅长理解复杂任务和多步骤规划。但相比GPT模型，它们通常运行速度更慢、成本更高。
GPT模型速度快、成本低且智能程度高，但在完成任务时对具体操作指令的依赖性更强。
大型（大模型）与小型（迷你或纳米模型）在速度、成本和智能水平之间存在权衡。大型模型在理解提示和跨领域解决问题方面表现更优，而小型模型通常运行更快且成本更低。

# 提示工程

提示工程是指为模型编写有效的指令，使其能够持续生成符合您需求的内容。

由于模型生成的内容具有不确定性，因此要获得期望的输出，需要结合艺术与科学。不过，您可以运用一些技巧和最佳实践，以确保结果的一致性。

某些提示工程技术适用于所有模型，例如使用消息角色。但不同类型的模型（如推理型模型与GPT模型）可能需要不同的提示方式才能获得最佳效果。即使同一类模型的不同版本，也可能产生不同的结果。因此，在构建更复杂的应用时，我们强烈建议：

- 将生产应用固定到特定的模型快照（例如 gpt-4.1-2025-04-14），以确保行为一致；
- 构建测试和评估套件，用于衡量提示行为，以便在迭代过程中或更改、升级模型版本时持续监控性能。

# 消息角色与指令遵循 Message roles and instruction following

消息角色与指令遵循

您可以通过指令API参数或消息角色向模型提供不同层级的权威性指令。

指令参数可为模型在生成响应时提供高层级的行为指导，包括语气、目标以及正确响应的示例。通过此方式提供的任何指令将优先于输入参数中的提示。

Generate text with instructions

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-6-astra",
    reasoning={"effort": "low"},
    instructions="Talk like a pirate.",
    input="Are semicolons optional in JavaScript?",
)

print(response.output_text)
```
上述示例大致相当于在输入数组中使用以下 input 参数输入消息：
```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="deepseek-flash",  # 模型选择
    reasoning={"effort": "low"},
    instructions="Talk like a pirate.",
    input=[
        {"role": "developer", "content": "Talk like a pirate."},
        {"role": "user", "content": "Are semicolons optional in JavaScript?"},
    ],
)

print(response.output_text)
```
OpenAI 模型规范描述了我们的模型如何根据不同角色的消息给予不同优先级。

role: developer 开发者消息是由应用程序开发者提供的指令，优先于用户消息。
role: user 用户消息是由终端用户提供的指令，其优先级低于开发者消息。
role: assistant 模型生成的消息具有助手角色。

多轮对话可能包含多种此类消息，以及您和模型提供的其他内容类型。

您可以将开发者消息和用户消息类比为编程语言中的函数及其参数。

developer 开发者消息提供系统的规则和业务逻辑，类似于函数定义；  
user 用户消息则提供输入和配置，供开发者消息指令所使用，类似于函数的参数。

## 在代码中管理提示

将生产环境中的提示存储在应用程序代码中，而不是创建可复用的提示对象。通过代码管理的提示，您可以使用类型化输入、代码审查、测试以及常规部署流程来修改模型行为。

对于新的提示工程工作：

- 将提示构建器封装在支持功能附近的独立小模块中。
- 对客户数据、文件或任务选项等动态值，使用类型化函数参数或模式。
- 直接将生成的指令和输入传递给响应 API。
- 在更改生产环境提示前，添加代表性的测试用例、测试和评估检查。
- 通过部署系统逐步实施提示变更，必要时使用功能标志或配置实现分阶段发布。
- 如果您的集成已调用具有提示 ID 或版本的保存提示，请参考提示对象迁移指南，将该提示移入代码。

# 使用markdown 或 xml 消息格式化处理
Message formatting with Markdown and XML

在撰写开发者和用户消息时，你可以通过结合 Markdown 格式和 XML 标签，帮助模型理解提示内容和上下文数据的逻辑边界。

Markdown 的标题和列表有助于标记提示的不同部分，并向模型传达层级结构。它们还能在开发过程中提升提示的可读性。XML 标签可用于明确某一段内容（例如用于参考的支持性文档）的起止位置。XML 属性还可用于定义提示中内容的元数据，以便后续指令引用。

通常情况下，开发者消息应包含以下部分，顺序如下（但具体最佳内容和顺序可能因所用模型而异）：

- Identity 身份信息：描述助手的目的、沟通风格以及总体目标。
- Instructions 指令说明：指导模型生成你期望的回答。应遵循哪些规则？模型应做什么，又不应做什么？此部分可根据你的使用场景包含多个子项，例如模型应如何调用自定义函数。
- Examples 示例：提供可能的输入示例，以及模型期望的输出结果。  
- Context 上下文：向模型提供任何额外信息，以帮助其生成响应，例如训练数据之外的私有/机密数据，或你认为特别相关的其他数据。通常这类内容应放在提示的末尾附近，因为不同生成请求可能需要不同的上下文。

以下是一个使用 Markdown 和 XML 标签构建开发者消息的示例，包含多个独立部分及支持性示例。
```ini
# 身份

你是一个编码助手，用于强制在 JavaScript 代码中使用蛇形命名法（snake case），并编写可在 Internet Explorer 6 版本上运行的代码。

# 指令

* 定义变量时，请使用蛇形命名（例如：my_variable），而不是驼峰命名（例如：myVariable）。
* 为支持旧版浏览器，请使用较早的“var”关键字声明变量。
* 不要返回带有 Markdown 格式的响应，仅按要求返回代码。

# 示例

<用户查询>
如何声明一个用于名字的字符串变量？
</用户查询>

<助手回复>
var first_name = "Anna";
</助手回复>
```

对应的代码如下：
```python
from openai import OpenAI

client = OpenAI()

with open("prompt.txt", "r", encoding="utf-8") as f:
    instructions = f.read()

response = client.responses.create(
    model="gpt-6-astra",
    instructions=instructions,
    input="How would I declare a variable for a last name?",
)

print(response.output_text)
```

# 通过提示缓存节省成本和延迟

在构建消息时，应尽量将预计会频繁使用的数据内容放在提示的开头，并作为JSON请求体中传递给Chat Completion或Response的第一个API参数。这样可以最大限度地利用提示缓存来降低使用成本和延迟。

# 少样本学习

少样本学习允许您通过在提示中包含少量输入/输出示例，引导大型语言模型完成新任务，而无需对模型进行微调。模型会隐式地从这些示例中“捕捉”出模式，并将其应用于新的提示中。在提供示例时，应尽量展示多种可能的输入及其对应的期望输出。

通常情况下，您会在 API 请求中的开发者消息中提供示例。以下是一个开发者消息示例，其中包含用于指导模型分类正面或负面客户服务评论的示例。

```ini
# Identity

You are a helpful assistant that labels short product reviews as
Positive, Negative, or Neutral.

# Instructions

* Only output a single word in your response with no additional formatting
  or commentary.
* Your response should only be one of the words "Positive", "Negative", or
  "Neutral" depending on the sentiment of the product review you are given.

# Examples

<product_review id="example-1">
I absolutely love this headphones — sound quality is amazing!
</product_review>

<assistant_response id="example-1">
Positive
</assistant_response>

<product_review id="example-2">
Battery life is okay, but the ear pads feel cheap.
</product_review>

<assistant_response id="example-2">
Neutral
</assistant_response>

<product_review id="example-3">
Terrible customer service, I'll never buy from them again.
</product_review>

<assistant_response id="example-3">
Negative
</assistant_response>
```

# 包含相关上下文信息

在给模型提供提示时，添加一些额外的上下文信息通常很有帮助，这样模型就能据此生成更合适的回复。这样做有以下几个常见原因：

- 为模型提供专有数据，或训练数据集之外的其他数据；
- 将模型的回应限制在你认为最有益的一组资源范围内。

向模型生成请求中添加更多相关上下文的技术有时被称为“检索增强生成”（RAG）。你可以通过多种方式向提示中加入额外上下文，例如查询向量数据库并将返回的文本内容纳入提示中，或者使用 OpenAI 内置的文件搜索工具，根据上传的文档生成内容。

# 上下文窗口的规划

模型在生成请求时，只能处理其认为的上下文范围内的有限数据。这个内存限制称为“上下文窗口”，通常以标记（即你输入的数据片段，从文本到图像）为单位来定义。

不同模型的上下文窗口大小各不相同，从低至10万标记，到较新的GPT-4.1模型可达一百万标记。具体每个模型的上下文窗口大小，请参阅对应模型的文档说明。

# 引导当前模型

像 gpt-6-astra 这样的 GPT 模型，需要明确的指令来提供完成任务所需的逻辑和数据。为了充分发挥最新模型的优势，请先参考gpt当前的提示指南。
https://developers.openai.com/api/docs/guides/latest-model


# 为最新模型提供最佳实践提示

如需获取当前完整的处理方法，请使用最新模型的最佳实践提示。以下实用提醒仍然适用。

## 编码

在提示 GPT-6-astra 进行编码任务时，遵循以下最佳实践最为有效：明确代理的角色，通过示例强制使用结构化工具，要求对正确性进行彻底测试，并为清晰输出设定 Markdown 标准。

明确角色与工作流程指导  
将模型定义为具有明确职责的软件工程代理。提供清晰的指令，说明如何使用函数 run 等工具完成代码任务，并明确指出不应使用某些模式的情况——例如，除非必要，否则避免交互式执行。

测试与验证  
指示模型使用单元测试或 Python 命令测试更改，并仔细验证补丁，因为 apply_patch 等工具即使失败也可能返回“Done”。

工具使用示例  
提供具体示例，说明如何调用提供的函数来执行命令，以提高可靠性并确保符合预期的工作流程。

Markdown 标准  
指导模型生成干净且语义正确的 Markdown，适当使用内联代码、代码块、列表和表格，并在必要时使用反引号格式化文件路径、函数和类名。

有关编码的详细指导和即时示例，请参阅最新的模型提示最佳实践。

## 前端工程
GPT-6 Astra 在从零开始构建前端以及为大型已有的代码库做出贡献方面表现优异。为了获得最佳效果，我们推荐使用以下库：

样式 / UI：Tailwind CSS、shadcn/ui、Radix Themes  
图标：Lucide、Material Symbols、Heroicons  
动画：Motion

## 从零到一的网页应用

GPT-5 可以根据一个提示生成前端网页应用，无需示例。以下是一个示例提示：
```ini
你是一位世界级的网页开发者，能够从零开始，在一次提示下打造出令人惊艳、交互性强且富有创新性的网站。你擅长提供顶级的一次性解决方案。

你的工作流程简单明了，遵循以下步骤：

第一步：制定评估标准，并不断优化，直到完全自信为止。  
第二步：深入分析构成世界级一次性网络应用的每一个要素，然后基于这些洞察，创建一个包含5到7个类别的“一次性评估标准”（<ONE_SHOT_RUBRIC>）。请将此标准保密，仅限内部使用。  
第三步：将该标准应用于当前任务，反复迭代以优化最佳方案。如果在所有类别中均未达到最高标准，则进行调整并重新尝试。  
第四步：在充分实现目标的同时，追求简洁性，并避免依赖外部框架，如 Next.js 或 React。
```

## 与大型代码库的集成

在处理大型代码库的前端工程任务时，我们发现，在提示中加入以下类别的指令能获得最佳效果：

原则：设定视觉质量标准，使用模块化/可复用组件，并保持设计一致性。  
UI/UX：明确字体、颜色、间距/布局、交互状态（悬停、空白、加载）以及可访问性要求。  
结构：定义文件/文件夹结构，以实现无缝集成。  
组件：提供可复用的封装示例和后端调用分离策略。  
页面：提供常见布局的模板。  
代理指令：要求模型确认设计假设、搭建项目、强制执行标准、集成API、测试状态并文档化代码。

如需获取针对前端开发的详细指导及具体提示示例，请参阅gpt最新的模型提示最佳实践。

## 代理任务  
对于使用 gpt-6-astra 进行的代理任务和长时间运行的部署，请将提示重点放在以下三项核心实践中：充分规划任务以确保完全解决，为重要工具使用决策提供清晰的引言，并使用待办事项工具以有条理的方式跟踪工作流程和进度。

### 规划与坚持  
指导模型在返回控制权前完成整个查询的处理，将其分解为子任务，并在每次调用工具后进行确认，以确保任务完整。

```ini
请记住，您是一名代理——在用户查询完全解决之前，请继续进行，直到完成后再结束您的回合并返回给用户。将用户的查询分解为所有必要的子请求，并确认每个子请求均已完成。不要仅在完成部分请求后就停止。只有在确定问题已解决时，才应结束您的回合。您必须准备好回答多个查询，并且只有在用户确认完成之后，才能结束通话。

在调用后续函数之前，您必须根据工作流程步骤进行充分规划，并对每次函数调用的结果进行深入反思，确保用户的查询及相关子请求均已完全解决。
```

## 透明度前言

请模型解释为何调用某个工具，但仅在关键步骤时说明。
```ini
Before you call a tool explain why you are calling it
```

## 使用评分标准和待办事项进行进度跟踪

使用待办事项清单工具或评分标准来确保有条不紊的规划，避免遗漏步骤。有关构建代理的具体详细指导和示例，请参阅最新的模型提示最佳实践。

## 提示推理模型

在提示推理模型与提示GPT模型时，存在一些需要考虑的差异。总体而言，推理模型在仅需高层次指导的任务上表现更佳，而GPT模型则能从非常明确的指令中获益。

你可以这样理解推理模型与GPT模型之间的区别：

推理模型就像一位资深同事，你可以给他们一个目标，然后信任他们去完成细节工作。

GPT模型则像一位初级同事，只有明确的指示才能产生特定输出，其表现才最出色。

如需了解使用推理模型的最佳实践，请参阅本指南。https://developers.openai.com/api/docs/guides/reasoning-best-practices

下一步

现在你已经了解了文本输入和输出的基本知识，接下来可以查看以下资源之一。

## 其他资源
https://developers.openai.com/cookbook

## 从提示对象迁移
将管理的提示对象使用方式移至应用程序代码中。

为了从 OpenAI API 平台的提示（Prompts）中迁移，将提示内容从托管的提示对象中移出，并移入您的应用程序代码中。这样可以更好地控制审核、测试、部署和版本管理。

之前：使用提示对象
```python
# Replace the illustrative IDs and URLs below with your own resource values.

from openai import OpenAI

client = OpenAI()
prompt_id = "pmpt_123"

response = client.responses.create(
    prompt={
        "prompt_id": prompt_id,
        "version": "1",
        "variables": {
            "customer_name": "Acme",
            "issue": "billing question",
        },
    }
)
```
之后：将提示语嵌入代码中
```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-6-astra",
    input=[
        {
            "role": "system",
            "content": "You are a helpful support assistant. Be concise, accurate, and friendly.",
        },
        {
            "role": "user",
            "content": "Customer name: Acme. Issue: billing question. Write a response to the customer.",
        },
    ],
)

print(response.output_text)
```

## 使用 Codex 进行迁移  
使用 OpenAI 开发者插件和 OpenAI Docs 技能，自动化您的迁移流程，加速使用 OpenAI API 的开发工作。
```ini
$openai-docs update this project to store prompts in code instead of using a prompts object
```
哪些内容发生了变化

- 不再通过 API 请求引用已保存的提示对象，而是将提示文本存储在代码库中，并直接将生成的消息作为输入传递给 Responses API 调用。
- 将提示内容移至源代码中，使提示的修改能够像产品逻辑一样经过相同的评审和发布流程。
- 用函数参数替换提示变量，使动态值在应用中显式且类型化。
- 在 Responses API 调用中通过输入传递消息，而不是使用提示对象。
- 使用 Git 提交、PR 评审以及测试或评估来管理版本控制。
- 将静态内容放在前面，动态内容放在后面，以保留提示缓存的优势，因为缓存命中依赖于精确的前缀匹配。

示例如下：
```python
from openai import OpenAI

# Build prompts with a helper function
client = OpenAI()


def build_support_prompt(customer_name, issue):
    return [
        {
            "role": "system",
            "content": "You are a helpful support assistant. Be concise, accurate, and friendly. Do not invent policy details.",
        },
        {
            "role": "user",
            "content": f"Customer name: {customer_name}. Issue: {issue}. Write a response to the customer.",
        },
    ]


response = client.responses.create(
    model="gpt-6-astra",
    input=build_support_prompt(
        customer_name="Acme", # 传递自定义的名字
        issue="billing question", # 传递 issue 到模版函数中
    ),
)
```

对应的go代码如下：
```go
package main

import (
	"context"
	"fmt"

	"github.com/openai/openai-go/v3"
	"github.com/openai/openai-go/v3/responses"
)

func main() {
    // 创建 go openai client
	client := openai.NewClient(
		option.WithBaseURL(os.Getenv("OPENAI_BASE_URL")),
		option.WithAPIKey(os.Getenv("OPENAI_API_KEY")),
	)

    // 发送请求
	response, err := client.Responses.New(context.Background(), responses.ResponseNewParams{
		Model: "gpt-6-astra",
		Input: responses.ResponseNewParamsInputUnion{OfInputItemList: buildSupportPrompt("Acme", "billing question")},
	})
	if err != nil {
		panic(err)
	}

    // 输出结果
	fmt.Println(response.OutputText())
}

func buildSupportPrompt(customerName string, issue string) responses.ResponseInputParam {
	return responses.ResponseInputParam{
		responses.ResponseInputItemParamOfMessage("You are a helpful support assistant. Be concise, accurate, and friendly. Do not invent policy details.", responses.EasyInputMessageRoleSystem),
		responses.ResponseInputItemParamOfMessage(fmt.Sprintf("Customer name: %s. Issue: %s. Write a response to the customer.", customerName, issue), responses.EasyInputMessageRoleUser),
	}
}
```
执行 `go run helper.go` 命令，运行结果如下：
```ini
Subject: Re: Your billing question

Hi Acme,

Thanks for reaching out. I’m happy to help with your billing question.

To make sure I review the correct account, could you please share:
- Your account or invoice number
- The date and amount in question
- A brief description of what you’d like us to check or clarify

Once I have those details, I’ll look into it and follow up with you.

Best regards,
[Your Name]
[Support Team]
```


你将获得的优势

你可以实现更紧密的工程控制：提示（prompts）与产品代码同步，变更通过 PR 进行，测试和评估可在 CI 中运行，而发布或实验则可通过自定义配置或功能标志进行管理。

不要在代码库中随意插入提示。请创建一个独立的提示模块，将每个提示作为命名的构建函数，并添加轻量级的评估测试用例，使提示的修改像产品逻辑一样接受审查。

# Citation Formatting 引用格式
https://developers.openai.com/api/docs/guides/citation-formatting

允许模型生成可靠的引用。

可靠的引用有助于建立信任，并帮助读者验证回答的准确性。本指南提供了实用指导，说明如何准备可引用的内容，并指导模型使用OpenAI模型熟悉的格式模板，有效生成引用。

## 概述

引用系统包含多个部分：你需要决定哪些内容可以被引用，清晰地呈现这些材料，指导模型如何进行引用，并在结果呈现给用户之前验证其准确性。

本指南涵盖模型直接体验到的五个核心要素：

可引用单元：明确模型允许引用的内容。
材料呈现：以清晰、结构化的方式展示原始资料。
引用格式：指定模型应使用的精确引用格式。
提示说明：告知模型何时引用以及如何正确引用。
引用解析：从模型的响应中提取引用信息，以便后续使用。

Choose citable units 选择可引用的单位

在编写提示前，需明确模型可以引用的内容。常见选项包括：

| Citable unit | Best used for | Downside | Example |
|---|---|---|---|
| Document | You only need to show which document the answer came from. | Not very precise. | Cite the entire employee handbook when you only need to show which document supports the claim. |
| Block / chunk | You want a good balance between simplicity and precision. | Still not exact down to the line. | Cite the specific contract paragraph or retrieved chunk that contains the clause. |
| Line range | You need to show the exact supporting text. | More difficult for the model. | Cite lines L42–L47 when the user needs to verify the precise passage. |

一个良好的可引用单元应具备以下特点：
- 一致性：同一来源在不同运行中应保持相同的ID。  
- 易于检查：人员应能够阅读并理解其上下文环境。  
- 适当大小：足够大以确保意义明确，但又足够小以保持精确性。
- 对于大多数系统而言，块级引用是最佳默认选择。它们通常比行级引用对模型更易处理，也比文档级引用对用户更有用。

## 可引用的材料

该模型无法引用未清晰呈现的材料。无论材料来自工具还是直接注入，均需确保其具备以下内容：

稳定的来源标识符：如 file1 或 block1 等一致的标识符。  
可读文本：格式清晰、易于阅读的原始材料。  
元数据（可选）：包括网址、时间戳、标题及类似上下文信息。

```ini
Citation Marker: {CITATION_START}cite{CITATION_DELIMITER}file0{CITATION_STOP}
Title: Employee Handbook
URL: https://company.example/handbook
Updated: 2026-03-01

[L1] Employees may work remotely up to three days per week.
[L2] Additional remote days require manager approval.
[L3] Exceptions may apply for approved accommodations.
```
源ID与定位符：源ID是一个稳定、由模型生成的标识符，例如block1。定位符则是精确的UI渲染高亮内容，例如第8至13行或第21段。通常情况下，模型应输出源ID，而你的系统负责解析或渲染定位符。过早地将两者混合使用，往往会导致格式错误增加。

## 定义引用格式

您需要为模型生成的引用格式进行定义。请使用明确、一致且便于模型可靠复制的格式。

以下是我们的推荐引用格式及推荐标记。这些引用标记高度推荐，因为它们与我们模型训练所使用的标记非常接近。如果您选择不同的标记值，请尽量保持整体引用格式的相似性。

| Piece | What it does | Recommended |
|---|---|---|
| `CITATION_START` | Opens the citation marker. | `\ue200` |
| Citation family | Identifies the citation type. Use `cite` for all supported sources. | `cite` |
| `CITATION_DELIMITER` | Separates fields inside the marker. | `\ue202` |
| Source ID | Identifies the cited unit. `turn#` is the turn number. `item#` is the specific file, block, or URL. | `turn0file1`, `turn0block1`, `turn0url1` |
| Locator (optional) | Narrows the citation to a precise span. | `L8–L13` |
| `CITATION_STOP` | Closes the citation marker. | `\ue201` |

对于工具调用，turnN 的计数是每次工具调用时递增一次，而不是每次单独结果时递增一次。在单次调用中，源文件会通过后缀进行区分，例如 file0、file1 等。在一个单响应系统中，如果模型在回答前恰好调用一次工具，则所有引用将为 turn0……；如果模型调用多次工具，则可能会看到类似 turn0fileX、turn1fileX 等的引用。

Template
```ini
{CITATION_START}<citation_family>{CITATION_DELIMITER}<source_id>{CITATION_DELIMITER}<locator>{CITATION_STOP}
```

Example

```ini
{CITATION_START}cite{CITATION_DELIMITER}turn0file1{CITATION_DELIMITER}L8-L13{CITATION_STOP}
```
如果您的系统未使用定位器，请省略该字段：
```ini
{CITATION_START}cite{CITATION_DELIMITER}turn0file1{CITATION_STOP}
```

## 编写有效的引用说明
为保持最高准确性，请使用熟悉的引用格式。自定义或不熟悉的格式会增加模型的认知负担，从而导致引用错误，尤其是在以下情况：

推理开销较低时，模型在纠正格式错误方面的恢复能力较弱；
高复杂度任务中，大部分推理预算用于完成任务本身，而非清理引用语法。

下面推荐一种接近模型已熟悉模式的引用格式。您可以直接使用，也可根据自身系统进行调整。

如果您希望自定义提示内容，请明确以下信息：
- 精确的标记语法；
- 引用的位置；
- 何时引用、何时不引用；
- 如何引用多个支持材料；
- 哪些格式被禁止；
- 当缺少支持材料时应如何处理。

# 提示生成
https://developers.openai.com/api/docs/guides/prompt-generation

# 前端提示说明 Frontend prompt instructions
复制粘贴指南，用于提升引导用户界面的质量，并避免常见的生成式界面默认设置。

本指南适用于 GPT-5.5，但其中许多模式同样适用于其他模型版本。
```ini
## Frontend guidance

You follow these instructions when building applications with a frontend experience:

### Build with empathy

- If working with an existing design or given a design framework in context, you pay careful attention to existing conventions and ensure that what you build is consistent with the frameworks used and design of the existing application.
- You think deeply about the audience of what you are building and use that to decide what features to build and when designing layout, components, visual style, on-screen text, and interaction patterns. Using your application should feel rich and sophisticated.
- You make sure that the frontend design is tailored for the domain and subject matter of the application. For example, SaaS, CRM, and other operational tools should feel quiet, utilitarian, and work-focused rather than illustrative or editorial: avoid oversized hero sections, decorative card-heavy layouts, and marketing-style composition, and instead prioritize dense but organized information, restrained visual styling, predictable navigation, and interfaces built for scanning, comparison, and repeated action. A game can be more illustrative, expressive, animated, and playful.
- You make sure that common workflows within the app are ergonomic, efficient, and comprehensive, so the user of your application can seamlessly navigate in and out of different views and pages in the application.

### Design instructions

- You make sure to use icons in buttons for tools, swatches for color, segmented controls for modes, toggles/checkboxes for binary settings, sliders/steppers/inputs for numeric values, menus for option sets, tabs for views, and text or icon+text buttons only for clear commands (unless otherwise specified). Cards are kept at 8px border radius or less unless the existing design system requires otherwise.
- You do not use rounded rectangular UI elements with text inside if you could use a familiar symbol or icon instead (examples include arrow icons for undo/redo, B/I icons for bold/italics, save/download/zoom icons). You build tooltips which name/describe unfamiliar icons when the user hovers over it.
- You use lucide icons inside buttons whenever one exists instead of manually-drawn SVG icons. If there is a library enabled in an existing application, you use icons from that library.
- You build feature-complete controls, states, and views that a target user would naturally expect from the application.
- You do not use visible, in-app text to describe the application's features, functionality, keyboard shortcuts, styling, visual elements, or how to use the application.
- You should not make a landing page unless absolutely required; when asked for a site, app, game, or tool, build the actual usable experience as the first screen, not marketing or explanatory content.
- When making a hero page, you use a relevant image, generated bitmap image, or immersive full-bleed interactive scene as the background with text over it that is not in a card; never use a split text/media layout where a card is one side and text is on another side, never put hero text or the primary experience in a card, never use a gradient/SVG hero page, and do not create an SVG hero illustration when a real or generated image can carry the subject.
- On branded, product, venue, portfolio, or object-focused pages, the brand/product/place/object must be a first-viewport signal, not only tiny nav text or an eyebrow. Hero content must leave a hint of the next section's content visible on every mobile and desktop viewport, including wide desktop.
- For landing-page heroes, make the H1 the brand/product/place/person name or a literal offer/category; put descriptive value props in supporting copy, not the headline.
- Websites and games must use visual assets. You can use image search, known relevant images, or generated bitmap images instead of SVGs, unless making a game. Primary images and media should reveal the actual product, place, object, state, gameplay, or person; you refrain from dark, blurred, cropped, stock-like, or purely atmospheric media when the user needs to inspect the real thing. For highly specific game assets you use custom SVG/Three.js/etc.
- For games or interactive tools with well-established rules, physics, parsing, or AI engines, you use a proven existing library for the core domain logic instead of hand-rolling it, unless the user explicitly asks for a from-scratch implementation.
- You use Three.js for 3D elements, and make the primary 3D scene full-bleed or unframed and not inside a decorative card/preview container. Before finishing, you verify with Playwright screenshots and canvas-pixel checks across desktop/mobile viewports that it is nonblank, correctly framed, interactive/moving, and that referenced assets render as intended without overlapping.
- You do not put UI cards inside other cards. Do not style page sections as floating cards. Only use cards for individual repeated items, modals, and genuinely framed tools. Page sections must be full-width bands or unframed layouts with constrained inner content.
- You do not add discrete orbs, gradient orbs, or bokeh blobs as decoration or backgrounds.
- You make sure that text fits within its parent UI element on all mobile and desktop viewports. Move it to a new line if needed, and if it still does not fit inside the UI element, use dynamic sizing so the longest word fits. Text must also not occlude preceding or subsequent content. Despite this, you check that text inside a UI button/card looks professionally designed and polished.
- Match display text to its container: reserve hero-scale type for true heroes, and use smaller, tighter headings inside compact panels, cards, sidebars, dashboards, and tool surfaces.
- You define stable dimensions with responsive constraints (such as aspect-ratio, grid tracks, min/max, or container-relative sizing) for fixed-format UI elements like boards, grids, toolbars, icon buttons, counters, or tiles, so hover states, labels, icons, pieces, loading text, or dynamic content cannot resize or shift the layout.
- You do not scale font size with viewport width. Letter spacing must be 0, not negative.
- You do not make one-note palettes: avoid UIs dominated by variations of a single hue family, and limit dominant purple/purple-blue gradients, beige/cream/sand/tan, dark blue/slate, and brown/orange/espresso palettes; scan CSS colors before finalizing and revise if the page reads as one of these themes.
- You make sure that UI elements and on-screen text do not overlap with each other in an incoherent manner. This is extremely important because overlap can lead to a jarring user experience.

When building a site or app that needs a dev server to run properly, you start the local dev server after implementation and give the user the URL so they can try it. If there's already a server on that port, you use another one. For a website where just opening the HTML will work, you don't start a dev server, and instead give the user a link to the HTML file that can open in their browser.
```
中文：
```ini
## 前端指导

在构建具有前端体验的应用程序时，请遵循以下建议：

### 以同理心进行开发

- 如果使用现有设计或在特定上下文中获得设计框架，应仔细关注现有的规范，并确保所构建的内容与当前应用使用的框架和设计风格保持一致。
- 深入思考你所面向的用户群体，并据此决定需要实现的功能，在设计布局、组件、视觉风格、屏幕文字以及交互模式时加以体现。你的应用应让用户感受到丰富而精致的体验。
- 确保前端设计贴合应用的领域和主题内容。例如，SaaS、CRM及其他运营工具应呈现低调、实用且以工作为中心的风格，而非装饰性强或强调表现力的设计：避免使用过于突出的主视觉区域、过度装饰的卡片式布局以及营销风格的排版方式，而应优先考虑信息密度高但结构清晰、视觉风格简洁、导航可预测，并支持快速浏览、对比和重复操作的界面。游戏可以更具表现力、生动性、动画效果和趣味性。  
- 你确保应用程序中的常见工作流程符合人体工学，高效且全面，使用户能够无缝地在应用的不同视图和页面之间切换。

### 设计规范

- 使用按钮中的图标表示工具，色块表示颜色，分段控件表示模式，开关/复选框表示二元设置，滑块/步进器/输入框表示数值，菜单用于选项集合，标签页用于视图，仅在明确需要时才使用文本或图标+文本按钮进行清晰指令。除非现有设计系统另有要求，卡片边框圆角应保持在8像素或更小。  
- 如果可以使用熟悉的符号或图标替代，则避免在按钮内使用带文字的圆形矩形UI元素（例如：撤销/重做箭头图标、粗体/斜体B/I图标、保存/下载/缩放图标）。应创建当用户悬停时会显示名称或描述不熟悉图标的工具提示。  
- 当存在合适图标时，优先使用清晰易懂的图标代替手动绘制的SVG图标。如果现有应用中启用了库，应使用该库中的图标。  
- 构建功能完整、符合目标用户预期的控件、状态和视图。  
- 不使用应用内的可见文本来描述应用的功能、特性、快捷键、样式、视觉元素或使用方法。  
- 除非绝对必要，否则不应创建着陆页；当被要求提供网站、应用、游戏或工具时，应以实际可用体验作为首页，而非营销或说明性内容。  
- 创建英雄页面时，应使用相关图片、生成的位图图像或沉浸式全屏交互场景作为背景，并在上面添加非卡片形式的文字；切勿采用卡片一侧为文字、另一侧为媒体的分屏布局；切勿将英雄文案或核心体验置于卡片内；切勿使用渐变或SVG英雄页面；若真实或生成的图像足以传达主题，则不应创建SVG英雄插图。
- 在以品牌、产品、场所、作品集或物品为核心的页面中，品牌/产品/地点/物品必须在首屏即被识别，而不仅仅是微小的导航文字或眉毛。首页的主打内容在每个移动和桌面视口（包括宽屏桌面）上都应能隐约显示下一部分的内容。
- 对于着陆页的主视觉内容，H1标题应为品牌/产品/场所/人物名称，或明确的优惠/类别；描述性价值主张应出现在辅助文案中，而非标题本身。
- 网站和游戏必须使用视觉资源。除非是制作游戏，否则可以使用图片搜索、已知的相关图像或生成的位图图像替代SVG。主要图像和媒体应展示实际的产品、场所、物品、状态、玩法或人物；当用户需要查看真实内容时，应避免使用深色、模糊、裁剪、类似库存或纯粹氛围化的媒体。对于高度特定的游戏资源，应使用自定义的SVG、Three.js等技术。
- 对于规则清晰、具备物理引擎、解析系统或AI引擎的游戏或交互工具，应使用经过验证的现有库来实现核心逻辑，而非自行编写，除非用户明确要求从零开始实现。
- 使用 Three.js 实现 3D 元素，主 3D 场景应为全屏或无边框显示，且不应嵌入装饰性卡片或预览容器中。在完成前，需通过 Playwright 截图及跨桌面/移动视口的 canvas 像素检查，确保场景不为空、框架正确、可交互并能动态移动，且引用的资源按预期渲染，无重叠现象。  
- 不将 UI 卡片嵌入其他卡片中。不要将页面区域样式化为浮动卡片。仅在需要重复出现的独立项目或模态框时使用卡片。
```
