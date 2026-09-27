import os

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),  # DeepSeek
)

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# ---------- 工具定义 ----------


def google_serper(query: str) -> str:
    """搜索引擎"""
    resp = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
        json={"q": query, "num": 5},
        timeout=10,
    )
    data = resp.json()
    # 提取标题+摘要拼成文本
    snippets = [r.get("snippet", "") for r in data.get("organic", [])]
    return "\n".join(snippets) if snippets else "No results."


def calculator(expr: str) -> str:
    """计算器，直接交给 Python 算，比 LLM 口算可靠得多"""
    try:
        expr = expr.replace("^", "**")  # 补上这行
        return str(eval(expr, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"


TOOLS = {
    "Search": google_serper,
    "Calculator": calculator,
}

TOOL_DESC = """Search: 搜索引擎，输入查询语句，返回搜索结果摘要
Calculator: 计算器，输入数学表达式（如 4.5**0.23），返回计算结果"""

# ---------- ReAct 循环 ----------

PROMPT_TEMPLATE = """尽可能回答下列问题，你可以使用以下工具：

{tools}

使用以下格式：

Question: 输入的问题
Thought: 思考该怎么做
Action: 必须是 [{tool_names}] 之一
Action Input: 动作的输入
Observation: 动作返回的结果
...（这个 Thought/Action/Action Input/Observation 循环可以重复多轮）
Thought: 我现在知道最终答案了
Final Answer: 原始问题的最终答案

开始！

Question: {question}
Thought:{scratchpad}"""


def run_agent(question: str, max_steps: int = 6) -> str:
    scratchpad = ""
    for _ in range(max_steps):
        prompt = PROMPT_TEMPLATE.format(
            tools=TOOL_DESC,
            tool_names=", ".join(TOOLS),
            question=question,
            scratchpad=scratchpad,
        )
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            stop=["\nObservation:"],  # 让模型停在等待 Observation 的位置
        )
        output = resp.choices[0].message.content
        print(output)  # verbose 效果

        if "Final Answer:" in output:
            return output.split("Final Answer:")[-1].strip()

        # 解析 Action / Action Input
        try:
            action = output.split("Action:")[-1].split("\n")[0].strip()
            action_input = (
                output.split("Action Input:")[-1].split("\n")[0].strip().strip('"')
            )
        except IndexError:
            return f"解析失败，最后输出：{output}"

        if action not in TOOLS:
            return f"未知动作 {action}，最后输出：{output}"

        observation = TOOLS[action](action_input)
        scratchpad += output + f"\nObservation: {observation}\nThought:"

    return "超过最大步数，未得到最终答案"


answer = run_agent("奥利维亚·王尔德的男朋友是谁?他现在的年龄的0.23次方是多少?")
print("\n最终答案:", answer)
