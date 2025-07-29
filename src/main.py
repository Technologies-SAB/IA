from config import settings
import sys

def run_pipeline(step):
    if step == 'download':
        print("--- PASSO 1: BAIXANDO CONTEÚDO DO CONFLUENCE ---")
        from ingestion.download_html import download_confluence_content
        download_confluence_content()

    elif step == 'images':
        print("\n--- PASSO 2: Iniciando Processamento de OCR nas Imagens ---")
        from ingestion.download_html import download_confluence_content
        download_confluence_content()

    elif step == 'convert':
        print("\n--- PASSO 3: PROCESSANDO CONTEÚDO PARA MARKDOWN ---")
        from ingestion.html_to_md import process_and_convert_to_md
        process_and_convert_to_md()

    elif step == 'embed':
        from embedding.generate_embeddings import update_embedding
        print("--- PASSO 4: GERANDO EMBEDDINGS ---")
        update_embedding(settings.MD_FOLDER)
        print("✅ Embeddings gerados e salvos localmente.")

    elif step == 'models':
        from training.download_models import download_embeddings_model, download_llm_model
        print("--- PASSO 5: BAIXANDO MODELOS ---")
        download_embeddings_model()
        download_llm_model()
        print("✅ Modelos baixados e salvos com sucesso.")

    elif step == 'chat':
        from chatbot.response import Chatbot
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
                print(f"Host: {response}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
    else:
        print(f"Opção '{step}' não implementada neste fluxo simplificado.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_pipeline(sys.argv[1])
    else:
        print("Uso: python main.py [download|embed|models|chat]")