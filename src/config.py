from pydantic_settings import BaseSettings
import dotenv

dotenv.load_dotenv()

class Settings(BaseSettings):
    # Configurações do Confluence
    # Carrega as variáveis de ambiente necessárias para a configuração do Confluence
    CONFLUENCE_URL: str
    CONFLUENCE_USERNAME: str
    CONFLUENCE_API_TOKEN: str

    # Caminho para guardar os documentos
    CONFLUENCE_SAVE_FOLDER: str

    class Config:
        env_file = ".env"

    def __init__(self, **values):
        super().__init__(**values)
        if not self.CONFLUENCE_URL or not self.CONFLUENCE_USERNAME or not self.CONFLUENCE_API_TOKEN:
            raise ValueError("As variáveis de ambiente CONFLUENCE_URL, CONFLUENCE_USERNAME e CONFLUENCE_API_TOKEN devem ser definidas.")
        if not self.CONFLUENCE_SAVE_FOLDER:
            raise ValueError("A variável de ambiente CONFLUENCE_SAVE_FOLDER deve ser definida.")

settings = Settings()