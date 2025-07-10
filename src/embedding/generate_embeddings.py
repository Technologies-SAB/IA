import os
import numpy as np
import logging
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from config import settings

logging.basicConfig(
    filename='embeddings.log',
    filemode='w',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

logger.info(f"Carregando modelo de embedding: {settings.MODEL_NAME}")

model_path = os.path.join(settings.MODEL_DIR_BASE, settings.MODEL_NAME)

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Modelo de embeddings não encontrado em {model_path}. Execute download_models.py primeiro.")

model = SentenceTransformer(model_path)

logger.info("Modelo de embedding carregado com sucesso.")

FAISS_INDEX_PATH = os.path.join(settings.EMBEDDINGS_DIR, 'faiss.index')
FAISS_METADATA_PATH = os.path.join(settings.EMBEDDINGS_DIR, 'faiss_metadatas.pkl')

def text_splitter(text, chunk_size=300, chunk_overlap=50):
    """Divide o texto em chunks baseados em parágrafos para manter o contexto."""
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_text(text)

def update_embedding(md_directory):
    embeddings = []
    metadatas = []
    
    os.makedirs(settings.EMBEDDINGS_DIR, exist_ok=True)

    logger.info(f"Iniciando varredura de arquivos .md em: {md_directory}")
    
    all_files = [os.path.join(root, file) for root, _, files in os.walk(md_directory) for file in files if file.endswith(".md")]

    if not all_files:
        logger.warning("Nenhum arquivo .md encontrado!")
        return

    for path in all_files:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                full_text = f.read()
            
            chunks = text_splitter(full_text)
            
            if not chunks:
                logger.warning(f"Nenhum chunk de texto gerado para: {path}")
                continue

            chunk_embeddings = model.encode(chunks)
            
            for i, chunk in enumerate(chunks):
                embeddings.append(chunk_embeddings[i])
                metadatas.append({
                    "source": path,
                    "chunk_id": i,
                    "text": chunk
                })
            
            logger.info(f"✔ {len(chunks)} embeddings gerados para: {path}")

        except Exception as e:
            logger.error(f"Erro ao processar {path}: {e}")

    if not embeddings:
        logger.warning("Nenhum embedding foi gerado.")
        return
        
    arr = np.array(embeddings).astype('float32')
    
    with open(FAISS_METADATA_PATH, 'wb') as f:
        pickle.dump(metadatas, f)
    logger.info(f"Metadados salvos em {FAISS_METADATA_PATH}")

    if len(arr) > 0:
        dimension = arr.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(arr)
        faiss.write_index(index, FAISS_INDEX_PATH)
        logger.info(f"Índice FAISS salvo em {FAISS_INDEX_PATH} com {index.ntotal} vetores.")