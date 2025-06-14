import dotenv
import os

dotenv.load_dotenv()

# Configurações do Confluence
# Carrega as variáveis de ambiente necessárias para a configuração do Confluence
CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
if not CONFLUENCE_URL or not CONFLUENCE_USERNAME or not CONFLUENCE_API_TOKEN:
    raise ValueError("As variáveis de ambiente CONFLUENCE_URL, CONFLUENCE_USERNAME e CONFLUENCE_API_TOKEN devem ser definidas.")

# Caminho para guardar os documentos
SAVE_FOLDER = os.getenv("CONFLUENCE_SAVE_FOLDER", "./confluence_docs")
if not SAVE_FOLDER:
    raise ValueError("A variável de ambiente CONFLUENCE_SAVE_FOLDER deve ser definida.")


SPACE_KEYS = os.getenv("CONFLUENCE_SPACE_KEYS", "").split(",") if os.getenv("CONFLUENCE_SPACE_KEYS") else []
