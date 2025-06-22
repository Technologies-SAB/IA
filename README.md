# 🤖 Agente de IA Local Especializado (Offline, Customizado, CPU-based)

## 🎯 Objetivo do Projeto

Desenvolver um chatbot de IA 100% local, que funcione diretamente via CPU em um notebook pessoal, sem qualquer dependência de modelos externos (como GPT, Gemini, Claude etc.). O bot será treinado e utilizado exclusivamente com base na documentação interna da empresa **Hospitality Holding Investments, Lda.**, especializada no setor Hoteleiro.

---

## 🧩 Funcionalidades

- ✅ Execução 100% offline (sem chamadas externas) `██████████ 100%`
- ✅ Treinamento com base em documentação interna (HTML → Markdown) `██████████ 100%`
- ✅ Geração de embeddings locais com `sentence-transformers` `██████████ 100%`
- ✅ Recuperação semântica com RAG (FAISS ou ChromaDB) `░░░░░░░░░░ 0%`
- ✅ Execução e correção de scripts SQL `░░░░░░░░░░ 0%`
- ✅ Interpretação de imagens (OCR + descrição) `░░░░░░░░░░ 0%`
- ✅ Interface de atendimento via chatbot (Streamlit, Gradio ou FastAPI) `░░░░░░░░░░ 0%`

---

## 📁 Estrutura do Projeto

```bash
agente_ia_local/
│
├── data/                      # Documentação convertida, imagens, dados brutos
│   ├── html/                  # HTMLs baixados do Confluence         ██████████ 100%
│   ├── markdown/              # Arquivos convertidos para .md        ██████████ 100%
│   └── imagens/               # Tutoriais visuais e screenshots      ██████████ 100%
│
├── embeddings/                # Armazenamento de vetores e índices   ██████████ 100%
│
├── models/                    # Modelos LLM locais (GGUF, LoRA, etc.) ░░░░░░░░░░ 0%
│
├── src/                       # Código-fonte principal
│   ├── ingestion/             # Scripts de ingestão e conversão de dados
│   │   ├── html_to_md.py      # Conversão HTML → Markdown            ██████████ 100%
│   │   ├── download_html.py   # Download de páginas HTML             ██████████ 100%
│   │   └── download_images.py # Download de imagens                  ██████████ 100%
│   ├── processing/            # Pré-processamento, segmentação, limpeza
│   │   └── preprocess.py      #                                      ░░░░░░░░░░ 0%
│   ├── embeddings/            # Geração e armazenamento de embeddings
│   │   └── generate_embeddings.py #                                  ██████████ 100%
│   ├── rag/                   # Implementação do pipeline RAG
│   │   └── retriever.py       #                                      ░░░░░░░░░░ 0%
│   ├── chatbot/               # Interface e lógica de interação
│   │   ├── interface.py       # Streamlit, Gradio ou FastAPI         ░░░░░░░░░░ 0%
│   │   └── responder.py       # Geração de respostas                 ░░░░░░░░░░ 0%
│   ├── images/                # OCR e descrição de imagens
│   │   └── image_parser.py    #                                      ░░░░░░░░░░ 0%
│   ├── utils/                 # Utilitários gerais                   ██████████ 100%
│   │   ├── fetch_json.py      #                                      ██████████ 100%
│   │   ├── save_html.py       #                                      ██████████ 100%
│   │   └── clean_filename.py  #                                      ██████████ 100%
│   └── config.py              # Configurações globais do projeto     ██████████ 100%
│
├── scripts/                   # Scripts utilitários e de setup
│   └── setup_env.py           #                                      ░░░░░░░░░░ 0%
│
├── tests/                     # Testes unitários e de integração     ░░░░░░░░░░ 0%
│
├── requirements.txt           # Dependências do projeto              ██████████ 100%
├── README.md                  # Documentação do projeto              ██████████ 100%
└── .env                       # Variáveis de ambiente (se necessário)██████████ 100%
```

---

## ⚙️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Hospitality-Holding-Investments/IA.git
cd IA
```

2. Crie um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as Dependências
```bash
pip install -r requirements.txt
```

4. Compile o llama.cpp (se necessário):
```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp && make
```

---

## 🚀 Como Usar

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

---

## 🧠 Tecnologias Utilizadas

• Python 3.10+

• transformers, sentence-transformers

• langchain, faiss, chromadb

• llama.cpp, GGUF

• streamlit, gradio, fastapi

• pytesseract, Pillow

---

## 🛡️ Restrições Técnicas

• Nenhuma dependência de nuvem (OpenAI, Google, Microsoft, etc.)

• Execução local via CPU

• Armazenamento e inferência 100% offline

---

## 📌 Licença
Este projeto é de uso interno da empresa Hospitality Holding Investments.