import os
import numpy as np
import logging
from sentence_transformers import SentenceTransformer
import pickle
from config import settings
import faiss

# Configuração do logger
logging.basicConfig(
    filename='embeddings.log',
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Carrega o modelo de embeddings
model = SentenceTransformer(settings.MODEL_NAME)

FAISS_INDEX_PATH = os.path.join(settings.EMBEDDINGS_DIR, 'faiss.index')
FAISS_METADATA_PATH = os.path.join(settings.EMBEDDINGS_DIR, 'faiss_metadatas.pkl')

# Novo método: gerar e salvar embeddings localmente (em .pkl e FAISS)
def update_embedding(directory):
    found = False
    embeddings = []
    metadatas = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                found = True
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        vetor = model.encode(text)
                        embeddings.append(vetor)
                        metadatas.append({"path": path})
                        logger.info(f"✔ Embedding gerado para: {path}")
                except Exception as e:
                    logger.error(f"Erro ao processar {path}: {e}")
    if not found:
        logger.warning("Nenhum arquivo .md encontrado!")
    else:
        arr = np.array(embeddings).astype('float32')
        np.save(os.path.join(settings.EMBEDDINGS_DIR, 'embeddings.npy'), arr)
        with open(os.path.join(settings.EMBEDDINGS_DIR, 'metadatas.pkl'), 'wb') as f:
            pickle.dump(metadatas, f)
        logger.info(f"Total de embeddings salvos: {len(embeddings)}")
        # FAISS
        if len(arr) > 0:
            index = faiss.IndexFlatL2(arr.shape[1])
            index.add(arr)
            faiss.write_index(index, FAISS_INDEX_PATH)
            with open(FAISS_METADATA_PATH, 'wb') as f:
                pickle.dump(metadatas, f)
            logger.info(f"Índice FAISS salvo com {index.ntotal} vetores.")

# Novo método: listar documentos dos embeddings salvos localmente
def listar_documentos_local(n=5):
    try:
        with open(os.path.join(settings.EMBEDDINGS_DIR, 'metadatas.pkl'), 'rb') as f:
            metadatas = pickle.load(f)
        count = len(metadatas)
        logger.info(f"Total de documentos salvos: {count}")
        for i, meta in enumerate(metadatas[:n]):
            logger.info(f"Documento {i+1}: Caminho: {meta['path']}")
    except Exception as e:
        logger.warning(f"Não foi possível listar documentos locais: {e}")

# Função para buscar documentos similares usando FAISS
def buscar_similares_faiss(query, top_k=5):
    if not os.path.exists(FAISS_INDEX_PATH) or not os.path.exists(FAISS_METADATA_PATH):
        logger.error("Índice FAISS ou metadados não encontrados.")
        return []
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(FAISS_METADATA_PATH, 'rb') as f:
        metadatas = pickle.load(f)
    query_vec = model.encode([query]).astype('float32')
    D, I = index.search(query_vec, top_k)
    resultados = []
    for idx, dist in zip(I[0], D[0]):
        if idx < len(metadatas):
            resultados.append({
                'path': metadatas[idx]['path'],
                'distancia': float(dist)
            })
    return resultados