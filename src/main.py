from ingestion.download_html import download_confluence_pages
from embeddings.generate_embeddings import update_embedding
from config import settings

if __name__ == "__main__":
    # download_confluence_pages()
    # print("✅ Processo de download e conversão concluído com sucesso!")

    update_embedding(settings.EMBEDDINGS_DIR)
    print("✅ Embeddings gerados e armazenados com sucesso no ChromaDB.")
