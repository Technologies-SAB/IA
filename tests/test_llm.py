import os
from langchain_community.llms import LlamaCpp

def run_minimal_test():
    """
    Executa um teste isolado para verificar a funcionalidade do LlamaCpp.
    """
    print("--- Iniciando teste mínimo do LLM ---")

    model_filename = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    model_path = os.path.join("models", "base", model_filename)

    if not os.path.exists(model_path):
        print(f"ERRO CRÍTICO: O arquivo do modelo não foi encontrado em '{model_path}'")
        print("Por favor, verifique se o arquivo está na pasta correta antes de continuar.")
        return

    print(f"Modelo encontrado: {model_path}")
    print("Tentando carregar o modelo com LlamaCpp...")

    try:
        llm = LlamaCpp(
            model_path=model_path,
            n_ctx=2048,           # Tamanho do contexto
            temperature=0.5,      # Um pouco de criatividade
            n_gpu_layers=0,       # Forçar CPU
            verbose=True,         # LIGAMOS O VERBOSE para obter o máximo de logs de depuração
            n_threads=4           # Defina um número de threads
        )
        print("\n✅ SUCESSO! Modelo LLM carregado sem erros.")
    except Exception as e:
        print(f"\n❌ FALHA AO CARREGAR O MODELO: {e}")
        return

    # 4. Invoque o modelo com o prompt mais simples possível
    prompt = "A capital da França é"
    print(f"\nEnviando prompt simples: '{prompt}'")
    print("Aguardando resposta do modelo...")

    try:
        response = llm.invoke(prompt)
        print("\n--- RESPOSTA DO MODELO ---")
        print(response)
        print("--------------------------")
        print("\n✅ SUCESSO! O teste foi concluído e o modelo respondeu.")
    except Exception as e:
        # Se o erro acontecer aqui, é durante a geração
        print(f"\n❌ ERRO DURANTE A GERAÇÃO DA RESPOSTA: {e}")

# Proteção essencial para o Windows
if __name__ == "__main__":
    run_minimal_test()