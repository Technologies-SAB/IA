from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import os
from config import settings

base_dir = settings.MODEL_DIR_BASE

def download_embeddings_model():
    embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_path = os.path.join(base_dir, embeddings_model_name)
    if os.path.exists(model_path) and os.listdir(model_path):
        print(f"Modelo de embeddings já existe em {model_path}, pulando download.")
        return
    embeddings_model = SentenceTransformer(embeddings_model_name)
    embeddings_model.save(model_path)
    print(f"Modelo de embeddings salvo em {model_path}")

def download_llm_model():
    llm_model_name = settings.LLM_NAME
    model_path = os.path.join(base_dir, llm_model_name)
    if os.path.exists(model_path) and os.listdir(model_path):
        print(f"Modelo LLM já existe em {model_path}, pulando download.")
        return
    llm_model = AutoModelForCausalLM.from_pretrained(llm_model_name)
    llm_tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
    llm_model.save_pretrained(model_path)
    llm_tokenizer.save_pretrained(model_path)
    print(f"Modelo LLM salvo em {model_path}")

os.makedirs(base_dir, exist_ok=True)
