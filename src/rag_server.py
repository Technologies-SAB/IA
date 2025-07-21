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
    from langdetect import detect, LangDetectException
    """
    prompt final para o LLM.
    """
    context_text = "\n\n---\n\n".join([item['text'] for item in context])
    try:
        detected_lang = detect(query)
        if detected_lang == 'pt':
            lang_instruction = "Responda em português."
        elif detected_lang == 'es':
            lang_instruction = "Responda em espanhol."
        else:
            lang_instruction = "Responda em inglês."
    except LangDetectException:
        lang_instruction = "Responda em inglês."

    prompt_template = f"""<s>[INST] Você é um assistente especialista em documentação técnica da empresa Hospitality Holding Investments. É especializado nos produtos: PMS (V10 e Host One), POS, Wellness, F&B, GXP, EMS e Access Gate.

    A sua função é responder exclusivamente com base na documentação técnica interna da empresa e no contexto fornecido.

    Instruções obrigatórias:
    - Nunca use os termos "bugs", "problemas" ou "erros" — utilize "situação identificada", "comportamento observado" ou equivalentes técnicos.
    - Responda sempre no mesmo idioma em que a PERGUNTA foi feita. Ou seja: {lang_instruction}
    - Se a informação solicitada não estiver disponível no CONTEXTO abaixo, responda com: "Não encontrei informações sobre isso na documentação." no idioma apropriado.
    - As respostas devem ser diretas, técnicas e orientadas à realidade dos produtos do ecossistema HOST.
    - Não emita pareceres fiscais, jurídicos ou técnicos externos ao ecossistema.
    - Mantenha um padrão formal e focado no processo.
    - Evite explicações teóricas sobre hotelaria. Sempre que possível, inicie com: “No sistema HOST, este processo é realizado da seguinte forma...”

    Sistemas da empresa:
    - **PMS V10 / Host One**: Sistema de gestão hoteleira multiunidade, cloud-based, com foco em personalização, relatórios estatísticos, reservas e experiências do hóspede.
    - **POS**: Sistema de ponto de venda integrado, com módulos de F&B, Kitchen Management, gestão de mesas, reservas e pagamentos. Compatível com GXP e PMS.
    - **Wellness**: Gestão de SPA e tratamentos, com agendamentos, relatórios, faturação integrada e reservas via Digital Keypass.
    - **F&B**: Operacionalização e gestão de alimentos e bebidas integrada com POS e PMS. Suporte a stock, faturação e reservas.
    - **GXP**: Ferramentas para melhorar a experiência digital do hóspede. Inclui Online Check-in, Self-Service Kiosk e Digital Keypass.
    - **EMS**: Gestão de eventos e catering, com foco em previsões de receita, reservas e emissão de documentação.
    - **Access Gate**: Solução de bilhética integrada para eventos, acessos e controlo de entradas com múltiplos canais de venda.
    - **Serviços HOST**: Suporte, formação, integrações e acompanhamento técnico especializado para todos os produtos do ecossistema.

    Responda com base exclusivamente no CONTEXTO abaixo e mantenha a objetividade.
        
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