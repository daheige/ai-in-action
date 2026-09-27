# 在LLM中调用函数

## 调用函数
函数调用是指可靠地连接LLM与外部工具的能力。让用户能够使用高效的外部工具、与外部API进行交互。

GPT-4和GPT-3.5是经过微调的LLM，能够检测函数是否被调用，随后输出包含调用函数参数的JSON。通过这一过程被调用的函数能够作为工具添加到您的AI应用中，并且您可以在单个请求中定义多个函数。

函数调用是一项重要能力。它对于构建LLM驱动的聊天机器人或代理至关重要。这些聊天机器人或代理需要为LLM检索上下文。它们还与外部工具交互。这种交互是通过将自然语言转换为API调用来完成的。

函数调用使开发者能够创建：

- 能够高效使用外部工具回答问题的对话代理。例如，查询“伯利兹的天气如何？”将被转换为类似get_current_weather(location: string, unit: 'celsius' | 'fahrenheit')的函数调用
- 用于提取和标记数据的LLM驱动解决方案（例如，从维基百科文章中提取人名）
- 可以帮助将自然语言转换为API调用或有效数据库查询的应用程序
- 能够与知识库交互的对话式知识检索引擎
  
# 示例
作为一个基本示例，假设我们要求模型检查特定地点的天气。

LLM本身无法响应此请求。因为它所使用的训练数据集截止至之前的某个日期。解决这个问题的方法是将LLM与外部工具结合起来。您可以利用模型的函数调用能力来确定要调用的外部函数及其参数，然后让它返回最终回复结果。以下是一个简单的示例，展示了如何使用OpenAI API实现这一点。

假设一个用户向模型提出以下问题：

伦敦的天气如何？

要使用函数调用处理此请求，第一步是定义一个或一组天气函数。您将作为OpenAI API请求的一部分传递这些函数：

```javascript
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string", 
                        "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },   
    }
]
```
说明：
- type 表示类型为function
- function的细节
  - name 表示名称
  - description 该函数的描述，作用
  - parameters 函数的参数信息
    - type 参数类型
    - properties 字段属性
      - location表示位置，属性字段
      - unit 字段，属性字段
    - required 表示哪些字段是必选参数字段

get_current_weather函数能够返回指定位置的天气情况。当您将这个函数定义作为请求的一部分传递时，它实际上并不执行函数，只是返回一个包含调用函数所需参数的JSON对象。以下是一些如何实现这一点的代码片段。

您可以如下定义一个完整的函数：
