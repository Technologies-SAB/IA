# 🤖 Agente de IA Local Especializado (Offline, Customizado, CPU-based)

## 🎯 Objetivo do Projeto

Desenvolver um chatbot de IA 100% local, que funcione diretamente via CPU em um notebook pessoal, sem qualquer dependência de modelos externos (como GPT, Gemini, Claude etc.). O bot será treinado e utilizado exclusivamente com base na documentação interna da empresa **Host Software International, Lda.**, especializada no setor Hoteleiro.

---

## 🧩 Funcionalidades

- ✅ Execução 100% offline (sem chamadas externas)
- ✅ Treinamento com base em documentação interna (HTML → Markdown)
- ✅ Geração de embeddings locais com `sentence-transformers`
- ✅ Recuperação semântica com RAG (FAISS ou ChromaDB)
- ✅ Execução e correção de scripts SQL
- ✅ Interpretação de imagens (OCR + descrição)
- ✅ Interface de atendimento via chatbot (Streamlit, Gradio ou FastAPI)

---

## 📁 Estrutura do Projeto
```bash
agente_ia_local/
│
├── data/                      # Documentação convertida, imagens, dados brutos
│   ├── html/                  # HTMLs baixados do Confluence
│   ├── markdown/              # Arquivos convertidos para .md
│   └── imagens/               # Tutoriais visuais e screenshots
│
├── embeddings/                # Armazenamento de vetores e índices FAISS/Chroma
│
├── models/                    # Modelos LLM locais (GGUF, LoRA, etc.)
│
├── src/                       # Código-fonte principal
│   ├── ingestion/             # Scripts de ingestão e conversão de dados
│   │   └── html_to_md.py
│   ├── processing/            # Pré-processamento, segmentação, limpeza
│   │   └── preprocess.py
│   ├── embeddings/            # Geração e armazenamento de embeddings
│   │   └── generate_embeddings.py
│   ├── rag/                   # Implementação do pipeline RAG
│   │   └── retriever.py
│   ├── chatbot/               # Interface e lógica de interação
│   │   ├── interface.py       # Streamlit, Gradio ou FastAPI
│   │   └── responder.py       # Geração de respostas
│   ├── images/                # OCR e descrição de imagens
│   │   └── image_parser.py
│   └── config.py              # Configurações globais do projeto
│
├── scripts/                   # Scripts utilitários e de setup
│   └── setup_env.py
│
├── tests/                     # Testes unitários e de integração
│
├── requirements.txt           # Dependências do projeto
├── README.md                  # Documentação do projeto
└── .env                       # Variáveis de ambiente (se necessário)
```
---

## ⚙️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/agente_ia_local.git
cd agente_ia_local
```

2. Crie um ambiente virtual:
```bash
python3 -m venv venv
souce venv/bin/activate
```

3. Instale as Dependências
```bash
pip install -r requirements.txt
```

4. Compile o llama.cpp (se necessário):
```bash
git cclone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp && make
```

🚀 Como Usar
1. Execute o pipeline de ingestão:
```bash
python src/ingestion/html_to_md.py
```

2. Gere os embeddings:
```bash
python src/embeddings/generate_embeddings.py
```

3. Inicie a interface do chatbot:
```bash
streamlit run src/chatbot/interface.py
```

## 🧠 Tecnologias Utilizadas

• Python 3.10+

• transformers, sentence-transformers

• langchain, faiss, chromadb

• llama.cpp, GGUF

• streamlit, gradio, fastapi

• pytesseract, Pillow


## 🛡️ Restrições Técnicas

• Nenhuma dependência de nuvem (OpenAI, Google, Microsoft, etc.)

• Execução local via CPU

• Armazenamento e inferência 100% offline

## 📌 Licença
Este projeto é de uso interno da empresa Host Software International, Lda.