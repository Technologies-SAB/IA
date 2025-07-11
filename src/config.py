from pydantic_settings import BaseSettings
import dotenv

dotenv.load_dotenv()

class Settings(BaseSettings):
    # Configurações do Confluence
    # Carrega as variáveis de ambiente necessárias para a configuração do Confluence
    CONFLUENCE_URL: str
    CONFLUENCE_USERNAME: str
    CONFLUENCE_API_TOKEN: str
    CONFLUENCE_SPACE_KEY: list[str]

    # Caminho para guardar os documentos
    CONFLUENCE_SAVE_FOLDER: str
    CONFLUENCE_MD_FOLDER: str
    CONFLUENCE_IMAGES_FOLDER: str

    # Configurações do banco de dados
    CHROMA_DB_DIR: str

    # Configuração do Embeddings
    MODEL_NAME: str
    EMBEDDINGS_DIR: str

    # Configurações LLM
    MODEL_DIR_BASE: str
    LLM_NAME: str = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    LLM_REPO_ID: str

    class Config:
        env_file = ".env"

    def __init__(self, **values):
        super().__init__(**values)
        if not self.CONFLUENCE_URL or not self.CONFLUENCE_USERNAME or not self.CONFLUENCE_API_TOKEN:
            raise ValueError("As variáveis de ambiente CONFLUENCE_URL, CONFLUENCE_USERNAME e CONFLUENCE_API_TOKEN devem ser definidas.")
        if not self.CONFLUENCE_SAVE_FOLDER:
            raise ValueError("A variável de ambiente CONFLUENCE_SAVE_FOLDER deve ser definida.")

settings = Settings()