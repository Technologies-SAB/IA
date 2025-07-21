import requests
from rag.retriever import FaissRetriever
from langdetect import detect, LangDetectException

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
    
        context_text = "\n\n---\n\n".join([item['text'] for item in context])
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
    
    def answer(self, query: str):
        context_chunks = self.retriever.search(query, top_k=7)
        if not context_chunks:
            return "Não encontrei informações relevantes na documentação."
        
        prompt = self._build_prompt(query, context_chunks)
        print("\n--- Enviando prompt para o servidor de LLM ---\n")
        print(prompt)

        final_response = self._call_llm_server(prompt)

        return final_response

