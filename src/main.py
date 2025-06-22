from ingestion.download_html import download_confluence_pages
from embeddings.generate_embeddings import update_embedding
from rag.retriever import search_similar_documents
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from config import settings

if __name__ == "__main__":
    # download_confluence_pages()
    # print("✅ Processo de download e conversão concluído com sucesso!")

    # update_embedding(settings.EMBEDDINGS_DIR)
    # print("✅ Embeddings gerados e armazenados com sucesso no ChromaDB.")

    embeder = SentenceTransformerEmbeddingFunction(settings.EMBEDDING_MODEL)
    query = "Como fazer login?"
    results = search_similar_documents(query, embeder, top_k=8)
    print(results)