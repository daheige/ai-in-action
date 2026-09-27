# pal 程序辅助语言模型
Gao 等人（2022）提出了一种使用 LLMs 读取自然语言问题并生成程序作为中间推理步骤的方法。被称为程序辅助语言模型（PAL），它与思维链提示不同，因为它不是使用自由形式文本来获得解决方案，而是将解决步骤卸载到类似 Python 解释器的编程运行时中。

## 创建虚拟环境
```shell
uv venv
source .venv/bin/activate
```

安装 openai 和 dotenv 库
```shell
uv pip install openai
uv pip install dotenv
```

导出依赖
```shell
uv pip freeze >> requirements.txt
```

从 requirements.txt 安装依赖
```shell
uv pip install -r requirements.txt
```

## 运行程序
.env配置文件如下：
```ini
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com/v1 # 为了方便学习，这里我使用deepseek api
```

```shell
python pal.py
```

输出结果如下：
```ini
02/27/1998
```

