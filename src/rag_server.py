import uvicorn
import requests
from fastapi import FastAPI
from pydantic import BaseModel

from rag.retriever import FaissRetriever

print("Iniciando o servidor RAG...")
try:
    retriever = FaissRetriever()
    print("✅ Retriever (FAISS + Embeddings) carregado com sucesso.")
except FileNotFoundError as e:
    print(f"❌ ERRO CRÍTICO: Não foi possível carregar o Retriever. {e}")
    print("    -> Certifique-se de que os embeddings foram gerados com 'python src/main.py embed'")
    exit()

LLM_SERVER_URL = "http://127.0.0.1:8000/generate"

app = FastAPI(
    title="Servidor de RAG e Perguntas",
    description="Uma API para conversar com o assistente de IA especializado."
)

class AskRequest(BaseModel):
    query: str
    top_k: int = 5

def _call_llm_server(prompt: str) -> str:
    """
    Função interna para fazer a requisição HTTP para o servidor do LLM.
    """
    try:
        response = requests.post(LLM_SERVER_URL, json={"prompt": prompt})
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            return f"Erro no servidor do LLM: {data['error']}"
        return data.get("response", "Nenhuma resposta recebida do servidor.")
    except requests.exceptions.RequestException as e:
        return f"ERRO DE COMUNICAÇÃO: Não foi possível conectar ao servidor do LLM. Detalhes: {e}"

def _build_prompt(query: str, context: list[dict]) -> str:
    """
    Constrói o prompt final para o LLM.
    """
    context_text = "\n\n---\n\n".join([item['text'] for item in context])
    prompt_template = f"""<s>[INST] Você é um assistente especialista na documentação da empresa Hospitality Holding Investments.
    - Sua tarefa principal é responder à pergunta do usuário baseando-se exclusivamente no CONTEXTO fornecido.
    - Se a informação não estiver no contexto, diga: "Não encontrei informações sobre isso na documentação."

    CONTEXTO:
    {context_text}

    PERGUNTA: {query} [/INST]
    """
    return prompt_template

@app.post("/ask", summary="Faz uma pergunta ao assistente de IA")
def ask_question(request: AskRequest):
    """
    Recebe uma pergunta (query), executa o pipeline RAG e retorna a resposta.
    """
    print(f"\n--- Recebida pergunta: '{request.query}' ---")
    
    print(f"Buscando contexto com top_k={request.top_k}...")
    context_chunks = retriever.search(request.query, top_k=request.top_k)
    if not context_chunks:
        return {"answer": "Não encontrei informações relevantes na documentação para responder a sua pergunta."}

    print("Construindo prompt para o LLM...")
    prompt = _build_prompt(request.query, context_chunks)
    
    context_for_log = "\n---\n".join([c['text'][:100] + '...' for c in context_chunks])
    print(f"Contexto enviado:\n{context_for_log}")

    print("Enviando prompt para o servidor do LLM...")
    final_response = _call_llm_server(prompt)
    
    print(f"Resposta final: {final_response}")

    return {"answer": final_response, "context_sources": [c['source'] for c in context_chunks]}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)