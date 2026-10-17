# 向量数据库
qdrant安装
```shell
docker run -itd -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```
- 端口 6333： REST API（HTTP）
- 端口 6334： gRPC API（适合批量操作，性能更高）
环境变量：
```shell
QDRANT__SERVICE__HTTP_PORT=6333
QDRANT__SERVICE__GRPC_PORT=6334
QDRANT__LOG_LEVEL=INFO
QDRANT__STORAGE__STORAGE_PATH=./qdrant/storage
```
卷/持久化存储： 挂载 ./qdrant/storage 用于数据持久化。如果不这样做，容器重启后数据将丢失。

验证qdrant是否正在运行
```shell
# 检查 Qdrant 是否正在运行
curl http://localhost:6333/

# 预期响应：
# {"title":"qdrant - vector search engine","version":"1.19.2","commit":"016542aa5deb6c66380bb137badf73d54f742bde"}

# 检查健康状态
curl http://localhost:6333/healthz

# 检查集群信息
curl http://localhost:6333/cluster
```

# python虚拟环境
```shell
uv venv myenv --python 3.12
# uv venv
uv pip install qdrant-client sentence-transformers openai numpy
uv pip list                         # 列出已安装包
uv pip show qdrant-client           # 查看包详情
uv pip freeze >> requirements.txt   # 导出 requirements 格式
```
如果虚拟环境已建立，可以安装对应的依赖包
```shell
uv pip install -r requirements.txt  # 从 requirements.txt 安装
```

# 编写 qdrant测试
```python
from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)
print(f"Qdrant connected: {client.get_collections()}")
```
运行效果如下：
```shell
python qdrant-demo.py
Qdrant connected: collections=[]
```

# 创建集合
```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    HnswConfigDiff,
    OptimizersConfigDiff,
    ScalarQuantization,  # ← 替换原来的 QuantizationConfig
    ScalarQuantizationConfig,
    ScalarType,
    VectorParams,
)

client = QdrantClient("localhost", port=6333)

client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1536,
        distance=Distance.COSINE,
        on_disk=False,
    ),
    hnsw_config=HnswConfigDiff(
        m=16,
        ef_construct=100,
        full_scan_threshold=10000,
    ),
    optimizers_config=OptimizersConfigDiff(indexing_threshold=20000),
    quantization_config=ScalarQuantization(  # ← 这里也换掉
        scalar=ScalarQuantizationConfig(
            type=ScalarType.INT8,
            quantile=0.99,
            always_ram=True,
        )
    ),
)

print("集合已创建！")
print(client.get_collection("documents"))
```

# 参考文档
https://qdrant.tech/documentation/quickstart/

# go 客户端
https://github.com/qdrant/go-client
