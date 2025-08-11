# 🤖 Agente de IA Local Especializado (Offline, Customizado, CPU-based)

## 🎯 Objetivo do Projeto
Desenvolver um chatbot de IA 100% local, que funcione diretamente via CPU em um notebook pessoal, sem qualquer dependência de modelos externos (como GPT, Gemini, Claude etc.). O bot será treinado e utilizado exclusivamente com base na documentação interna da empresa **Hospitality Holding Investments, Lda.**, especializada no setor Hoteleiro.

---

## 🧩 Funcionalidades

✅ Execução 100% offline (sem chamadas externas) ██████████ 100%

✅ Treinamento com base em documentação interna (HTML → Markdown) ██████████ 100%

✅ Geração de embeddings locais com sentence-transformers ██████████ 100%

✅ Download e gerenciamento automático de modelos (embeddings e LLM) ██████████ 100%

✅ Recuperação semântica com RAG (FAISS ou ChromaDB) ██████░░░░ 60%

✅ Interface de atendimento via chatbot (linha de comando, totalmente em português) ██████████ 100%

✅ Fine-tuning com LoRA usando peft █████░░░░░ 50%

✅ Interpretação de imagens (OCR + descrição) ░░░░░░░░░░ 0%

✅ Execução e correção de scripts SQL ░░░░░░░░░░ 0%

## 📁 Estrutura do Projeto

```bash
gente_ia_local/
│
├── data/                      # Documentação convertida, imagens, dados brutos ██████████ 100%
│   ├── html/                  # HTMLs baixados do Confluence
│   ├── markdown/              # Arquivos convertidos para .md
│   └── images/                # Tutoriais visuais e screenshots
│
├── log/                       # Logs de execução e erros
│
├── models/
│   ├── base/                  # Modelos LLM leves (GGUF, GPT2, etc.)
│
├── src/                       # Código-fonte principal
│   ├── ingestion/             # Scripts de ingestão e conversão de dados
│   │   ├── html_to_md.py      # Conversão HTML → Markdown            ██████████ 100%
│   │   ├── download_html.py   # Download de páginas HTML             ██████████ 100%
│   │   └── download_images.py # Download de imagens                  ██████████ 100%
│   ├── processing/            # Pré-processamento, segmentação, limpeza ░░░░░░░░░░ 0%
│   ├── embedding/             # Geração e armazenamento de embeddings ██████████ 100%
│   │   └── generate_embeddings.py #                                  ██████████ 100%
│   ├── rag/                   
│   │   └── retriever.py       # Implementação do pipeline RAG        ██████░░░░ 0%
│   ├── training/              # Download e fine-tuning de modelos    ██████████ 100%
│   │   └── download_models.py # Download automático de modelos       ██████████ 100%
│   ├── chatbot/               # Interface e lógica de interação      ██████████ 100%
│   │   ├── interface.py       # Streamlit, Gradio ou FastAPI         ░░░░░░░░░░ 0%
│   │   └── response.py        # Geração de respostas                 ██████████ 100%
│   ├── images/                # OCR e descrição de imagens           ░░░░░░░░░░ 0%
│   │   └── image_parser.py    #                                      ░░░░░░░░░░ 0%
│   ├── utils/                 # Utilitários gerais                   ██████████ 100%
│   │   ├── fetch_json.py      #                                      ██████████ 100%
│   │   ├── save_html.py       #                                      ██████████ 100%
│   │   └── clean_filename.py  #                                      ██████████ 100%
│   └── config.py              # Configurações globais do projeto     ██████████ 100%
│
├── scripts/                   # Scripts utilitários e de setup       ░░░░░░░░░░ 0%
│   └── setup_env.py           #                                      ░░░░░░░░░░ 0%
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

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

---

## 🚀 Como Usar (Pipeline Completo)

Execute cada etapa do pipeline pelo terminal:

1. Baixe a documentação do Confluence:
```bash
python src/main.py download
```

2. Gere os embeddings locais:
```bash
python src/main.py embed
```


3. Baixe os modelos necessários (embeddings e LLM):
```bash
python src/main.py models
```

4. Inicie o chatbot (linha de comando):
```bash
python src/main.py chat
```

5. Inicie o server LLM (em um novo terminal):
```bash
python src/llm_server.py
```

Durante o chat, digite 'sair' para encerrar a conversa.

---

## 🧠 Tecnologias Utilizadas

• Python 3.10+

• transformers, sentence-transformers

• langchain, faiss

• llama.cpp, GGUF

• streamlit, gradio, fastapi

• pytesseract, Pillow, BeautifulSoup

---

## 🛡️ Restrições Técnicas
• Nenhuma dependência de nuvem (OpenAI, Google, Microsoft, etc.)
• Execução local via CPU
• Armazenamento e inferência 100% offline

---

## 📌 Licença
Este projeto é de uso interno e de propriedade da SAB Technologies.