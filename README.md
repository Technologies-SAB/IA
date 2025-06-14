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