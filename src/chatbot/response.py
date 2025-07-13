import requests
from rag.retriever import FaissRetriever

class Chatbot:
    def __init__(self):
        print("Inicializando o Retriever...")
        self.retriever = FaissRetriever()
        self.llm_server_url = "http://127.0.0.1:8000/generate"
        print("✅ Retriever inicializado. O Chatbot usará o servidor de LLM.")

    def _call_llm_server(self, prompt: str) -> str:
        """
        Função auxiliar para fazer a requisição HTTP para o servidor do LLM.
        """
        try:
            response = requests.post(self.llm_server_url, json={"prompt": prompt})
            response.raise_for_status()
            data = response.json()
            if "error" in data:
                return f"Erro no servidor do LLM: {data['error']}"
            return data.get("response", "Nenhuma resposta recebida do servidor.")
        except requests.exceptions.RequestException as e:
            return f"ERRO DE COMUNICAÇÃO: Não foi possível conectar ao servidor do LLM em {self.llm_server_url}. Verifique se o llm_server.py está rodando. Detalhes: {e}"

    def _build_prompt(self, query: str, context: list[dict]) -> str:
        context_text = "\n\n---\n\n".join([item['text'] for item in context])
        prompt_template = f"""<s>[INST] Você é um assistente especialista na documentação da empresa Hospitality Holding Investments.
        - Sua tarefa principal é responder à pergunta do usuário baseando-se exclusivamente no CONTEXTO fornecido.
        - **NOVA REGRA:** Se o contexto mencionar múltiplos sistemas (como V10 e Host One) ou múltiplos métodos para uma mesma tarefa, e a pergunta do usuário for genérica, sua primeira resposta deve ser uma pergunta de esclarecimento. Por exemplo: "Para qual sistema você gostaria de saber o procedimento, V10 ou Host One?".
        - Se o contexto for claro e a pergunta específica, responda diretamente.
        - Se a informação não estiver no contexto, diga: "Não encontrei informações sobre isso na documentação."

        CONTEXTO:
        {context_text}

        PERGUNTA: {query} [/INST]
        """
        return prompt_template
    
    def answer(self, query: str):
        context_chunks = self.retriever.search(query, top_k=7)
        if not context_chunks:
            return "Não encontrei informações relevantes na documentação."
        
        prompt = self._build_prompt(query, context_chunks)
        print("\n--- Enviando prompt para o servidor de LLM ---\n")
        print(prompt)

        final_response = self._call_llm_server(prompt)

        return final_response

