from ingestion.download_html import download_confluence_pages
from embedding.generate_embeddings import update_embedding
from training.download_models import download_embeddings_model, download_llm_model
from chatbot.response import Chatbot # Importa a classe do chatbot
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
        print("--- PASSO 4: INICIANDO CHATBOT ---")
        try:
            bot = Chatbot()
            print("\n\nChatbot iniciado. Digite 'sair' para terminar.")
            while True:
                query = input("Você: ")
                if query.lower() == 'sair':
                    break
                response = bot.answer(query)
                print(f"Assistente: {response}")
        except FileNotFoundError as e:
            print(f"\nERRO: {e}")
            print("Certifique-se de ter executado os passos 'models' e 'embed' primeiro.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    else:
        print("Argumento inválido. Use 'download', 'embed', 'models' ou 'chat'.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_pipeline(sys.argv[1])
    else:
        print("Uso: python main.py [download|embed|models|chat]")