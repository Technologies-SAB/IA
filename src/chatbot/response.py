import os
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from config import settings
from rag.retriever import FaissRetriever # Importamos nosso retriever

class Chatbot:
    def __init__(self):
        self.retriever = FaissRetriever()

        llm_path = os.path.join(settings.MODEL_DIR_BASE, settings.LLM_NAME)
        if not os.path.exists(llm_path):
            raise FileNotFoundError(f"Modelo LLM não encontrado em {llm_path}. Execute download_models.py primeiro.")
        
        print("Carregando o modelo LLM local... Isso pode levar alguns minutos.")
        
        tokenizer = AutoTokenizer.from_pretrained(llm_path)
        model = AutoModelForCausalLM.from_pretrained(llm_path)

        self.llm_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,  
            device=-1 # Use -1 para CPU, ou 0 para GPU se disponível
        )
        print("Chatbot pronto para uso.")

    def _build_prompt(self, query: str, context: list[dict]) -> str:
        """
        Constrói o prompt final para o LLM, combinando a pergunta com o contexto recuperado.
        """
        context_text = "\n\n---\n\n".join([item['text'] for item in context])

        # Este template de prompt é crucial para obter boas respostas!
        prompt_template = f"""
Você é um assistente especialista na documentação da empresa Hospitality Holding Investments.
Sua tarefa é responder à pergunta do usuário de forma precisa e concisa, baseando-se exclusivamente no CONTEXTO fornecido.
Se a informação não estiver no contexto, responda educadamente que você não possui essa informação e que será necessário abrir um ticket para o suporte.
Gere scripts SQL apenas se o contexto contiver esquemas de tabelas e a pergunta pedir explicitamente por um.

CONTEXTO:
{context_text}

PERGUNTA DO USUÁRIO:
{query}

RESPOSTA:
"""
        return prompt_template

    def answer(self, query: str):
        # Passo 1: Recuperar (Retrieve)
        context_chunks = self.retriever.search(query, top_k=3)
        
        if not context_chunks:
            return "Não encontrei informações relevantes na documentação para responder a sua pergunta."

        # Passo 2: Aumentar (Augment)
        prompt = self._build_prompt(query, context_chunks)
        
        print("\n--- PROMPT ENVIADO PARA O LLM ---\n")
        print(prompt)
        print("\n--- GERANDO RESPOSTA... ---\n")

        # Passo 3: Gerar (Generate)
        generated_output = self.llm_pipeline(prompt)
        response = generated_output[0]['generated_text']
        
        # Limpa a resposta para remover o prompt inicial
        final_response = response.split("RESPOSTA:")[-1].strip()
        
        return final_response