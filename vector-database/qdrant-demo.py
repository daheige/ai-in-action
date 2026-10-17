from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)
print(f"Qdrant connected: {client.get_collections()}")
