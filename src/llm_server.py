import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import os

from langchain_community.llms import LlamaCpp
from config import settings

print("Iniciando o servidor de LLM...")
llm_path = os.path.join(settings.MODEL_DIR_BASE, settings.LLM_NAME)
if not os.path.exists(llm_path):
    raise FileNotFoundError(f"Modelo LLM (.gguf) não encontrado em {llm_path}.")

print("Carregando o modelo LLM... Este processo pode levar vários minutos.")
llm = LlamaCpp(
    model_path=llm_path, n_ctx=4096, n_gpu_layers=0, temperature=0.1,
    max_tokens=512, stop=["</s>", "[/INST]"], n_threads=4, verbose=False
)
print("✅ Modelo LLM carregado e pronto para receber requisições.")

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate_text(request: PromptRequest):
    """
    Recebe um prompt e retorna a geração do modelo.
    """
    try:
        print("\n--- Recebido prompt para geração ---")
        print(request.prompt)
        
        # Chama o modelo que já está carregado na memória
        response = llm.invoke(request.prompt)
        
        print("--- Resposta gerada ---")
        print(response)
        
        return {"response": response.strip()}
    except Exception as e:
        return {"error": f"Erro durante a geração: {e}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)