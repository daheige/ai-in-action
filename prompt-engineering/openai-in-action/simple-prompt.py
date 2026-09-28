import os

from openai import OpenAI

# 运行方式 python simple-prompt.py
# 或者 python simple-prompt.py >> rust.md
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

response = client.responses.create(
    model="deepseek-flash",  # 模型选择
    input="rust是什么？未来发展怎么样？",  # 输入
)

# 输出文本
print(response.output_text)
