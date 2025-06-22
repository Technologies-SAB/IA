from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import os
from src.config import settings

base_dir = settings.MODEL_DIR_BASE


def download_embeddings_model():
    embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings_model = SentenceTransformer(embeddings_model_name)
    embeddings_model.save(os.path.join(base_dir, embeddings_model_name))

def download_llm_model():
    llm_model_name = settings.LLM_NAME
    llm_model = AutoModelForCausalLM.from_pretrained(llm_model_name)
    llm_tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
    llm_model.save_pretrained(os.path.join(base_dir, llm_model_name))
    llm_tokenizer.save_pretrained(os.path.join(base_dir, llm_model_name))

os.makedirs(base_dir, exist_ok=True)
