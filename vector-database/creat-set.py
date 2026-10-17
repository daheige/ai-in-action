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

# SentenceTransformers 的集合（384 维）
client.create_collection(
    collection_name="embeddings_384",
    vectors_config=VectorParams(
        size=384,  # all-MiniLM-L6-v2 输出大小
        distance=Distance.COSINE,
    ),
)
