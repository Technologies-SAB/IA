import chromadb
from src.config import settings

chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
collection = chroma_client.get_or_create_collection(name="confluence_embeddings")

def search_similar_documents(query, embeder, top_k):
    query_embedding = embeder(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results