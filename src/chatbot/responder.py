import os
from src.embedding.generate_embeddings import buscar_similares_faiss
from config import settings
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Carrega o modelo LLM e o tokenizer
MODEL_PATH = settings.MODEL_DIR_BASE  # ajuste se necessário
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

def responder_pergunta(pergunta, top_k=3, max_tokens=500):
    # 1. Buscar documentos relevantes via FAISS
    docs = buscar_similares_faiss(pergunta, top_k=top_k)
    contexto = "\n".join([open(doc['path'], encoding='utf-8').read() for doc in docs if os.path.exists(doc['path'])])
    # 2. Montar prompt com contexto
    prompt = f"Contexto:\n{contexto}\n\nPergunta: {pergunta}\nResposta:"
    # 3. Gerar resposta com o LLM
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=max_tokens, do_sample=True)
    resposta = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Retorna apenas a resposta após o prompt
    resposta_final = resposta.split("Resposta:", 1)[-1].strip()
    return resposta_final
