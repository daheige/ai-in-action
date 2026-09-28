import os

from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    model="deepseek-flash",  # 模型选择
    reasoning={"effort": "low"},
    instructions="Talk like a pirate.",
    input=[
        {"role": "developer", "content": "Talk like a pirate."},
        {"role": "user", "content": "Are semicolons optional in JavaScript?"},
    ],
)

print(response.output_text)
