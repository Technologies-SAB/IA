from sentence_transformers import SentenceTransformer
import os
from config import settings
# Importamos a função específica para download
from huggingface_hub import hf_hub_download, HfApi

base_dir = settings.MODEL_DIR_BASE
os.makedirs(base_dir, exist_ok=True)

def download_embeddings_model():
    # Esta função já está correta, sem alterações.
    embeddings_model_name = settings.MODEL_NAME
    model_path = os.path.join(base_dir, embeddings_model_name)
    if os.path.exists(model_path) and os.listdir(model_path):
        print(f"Modelo de embeddings '{embeddings_model_name}' já existe, pulando download.")
        return
    
    print(f"Baixando modelo de embeddings: {embeddings_model_name}...")
    embeddings_model = SentenceTransformer(embeddings_model_name)
    embeddings_model.save(model_path)
    print(f"✅ Modelo de embeddings salvo em {model_path}")

def download_llm_model():
    llm_filename = settings.LLM_NAME
    llm_path = os.path.join(base_dir, llm_filename)

    # Se o arquivo já existe localmente, não fazemos nada.
    if os.path.exists(llm_path):
        print(f"✅ Modelo LLM '{llm_filename}' já existe localmente, pulando download.")
        return

    print(f"Modelo LLM '{llm_filename}' não encontrado localmente. Tentando baixar...")

    # Precisamos do nome do REPOSITÓRIO de onde o arquivo GGUF vem.
    # Exemplo de repositório: "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
    # Vamos criar uma variável para isso, talvez no .env ou hardcoded aqui.
    # Por agora, vamos deduzir do nome do arquivo, o que é um pouco frágil.
    # Uma abordagem melhor é ter REPO_ID e FILENAME no .env
    
    # Exemplo: Se LLM_NAME for "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    # O repositório é "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
    # Vamos adicionar uma nova configuração para isso.
    
    if not hasattr(settings, 'LLM_REPO_ID'):
        print("❌ ERRO: A configuração 'LLM_REPO_ID' não foi encontrada no seu .env ou config.py.")
        print("    Adicione LLM_REPO_ID='TheBloke/Mistral-7B-Instruct-v0.2-GGUF' ao seu arquivo .env")
        return

    repo_id = settings.LLM_REPO_ID
    filename = settings.LLM_NAME

    print(f"Baixando '{filename}' do repositório '{repo_id}'...")
    
    try:
        hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=base_dir,
            local_dir_use_symlinks=False,
            resume_download=True
        )
        print(f"✅ Download do modelo LLM concluído com sucesso! Salvo em: {llm_path}")
    except Exception as e:
        print(f"❌ Falha ao baixar o modelo LLM: {e}")
        print("    Verifique se o nome do repositório (LLM_REPO_ID) e do arquivo (LLM_NAME) estão corretos no seu arquivo .env.")