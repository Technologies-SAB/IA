from ingestion.download_html import download_confluence_pages
from embedding.generate_embeddings import update_embedding, listar_documentos_local
from training.download_models import download_embeddings_model, download_llm_model
from config import settings

if __name__ == "__main__":
    # download_confluence_pages()
    # print("✅ Processo de download e conversão concluído com sucesso!")

    # update_embedding(settings.EMBEDDINGS_DIR)
    # print("✅ Embeddings gerados e salvos localmente.")
    # listar_documentos_local()

    # download_embeddings_model()
    # print("✅ Modelo de embeddings baixado e salvo com sucesso.")
    # download_llm_model()
    # print("✅ Modelo LLM baixado e salvo com sucesso.")


