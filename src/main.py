from rag.retriever import FaissRetriever
from ingestion.download_html import download_confluence_pages
from embedding.generate_embeddings import update_embedding
from training.download_models import download_embeddings_model, download_llm_model
from chatbot.response import Chatbot
from config import settings
import sys

def run_pipeline(step):
    if step == 'download':
        print("--- PASSO 1: BAIXANDO DOCUMENTAÇÃO DO CONFLUENCE ---")
        download_confluence_pages()
        print("✅ Processo de download e conversão concluído com sucesso!")

    elif step == 'embed':
        print("--- PASSO 2: GERANDO EMBEDDINGS ---")
        # Passamos o diretório correto dos arquivos .md
        update_embedding(settings.CONFLUENCE_MD_FOLDER)
        print("✅ Embeddings gerados e salvos localmente.")

    elif step == 'models':
        print("--- PASSO 3: BAIXANDO MODELOS ---")
        download_embeddings_model()
        download_llm_model()
        print("✅ Modelos baixados e salvos com sucesso.")

    elif step == 'chat':
        print("--- INICIANDO CLIENTE DO CHATBOT ---")
        print("Certifique-se de que o servidor do LLM está rodando em outro terminal.")
        try:
            bot = Chatbot()
            print("\n\nChatbot iniciado. Digite 'sair' para terminar.")
            while True:
                query = input("Você: ")
                if query.lower() == 'sair':
                    break
                response = bot.answer(query)
                print(f"Assistente: {response}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
    else:
        print(f"Opção '{step}' não implementada neste fluxo simplificado.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_pipeline(sys.argv[1])
    else:
        print("Uso: python main.py [download|embed|models|chat]")