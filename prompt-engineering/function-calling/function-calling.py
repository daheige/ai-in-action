import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 创建客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),  # DeepSeek，直连 OpenAI 则删掉此行
)


# 定义调用函数
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather = {"location": location, "temperature": "50", "unit": unit}
    return json.dumps(weather)


# 工具定义，定义工具的基本参数设置
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
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]

# 工具名 -> 真实函数的映射
FUNCTIONS = {"get_current_weather": get_current_weather}

messages = [{"role": "user", "content": "What is the weather like in London?"}]

# ---------- tool calling 主循环 ----------
while True:
    # 创建openai请求
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        temperature=0,
        max_tokens=300,
    )

    # 获取返回的message
    msg = response.choices[0].message

    # 1. 模型没有要求调用工具 -> 循环结束
    if not msg.tool_calls:
        print(msg.content)
        break

    # 2. 把模型的"调用请求"加入历史
    messages.append(msg)

    # 3. 逐个执行工具，把结果作为 tool 消息返回
    for call in msg.tool_calls:
        fn_name = call.function.name
        args = json.loads(call.function.arguments)  # 参数是 JSON 字符串，要解析
        result = FUNCTIONS[fn_name](**args)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": call.id,  # 必须对应调用的 id
                "name": fn_name,
                "content": result,
            }
        )
