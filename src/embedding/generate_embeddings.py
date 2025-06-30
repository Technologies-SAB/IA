import os
import numpy as np
import logging
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions
from config import settings

# Configuração do logger
logging.basicConfig(
    filename='embeddings.log',
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

chroma_client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_DIR,
)

collection = chroma_client.get_or_create_collection(
    name="confluence_embeddings"
)

embeder = embedding_functions.SentenceTransformerEmbeddingFunction(settings.MODEL_NAME)

def update_embedding(directory):
    found = False
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                found = True
                path = os.path.join(root, file)
                #logger.info(f"Encontrado: {path}")
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        vetor = embeder(text)
                        if isinstance(vetor, np.ndarray) and len(vetor.shape) == 2:
                            vetor = vetor[0]
                        collection.add(
                            ids=[path],
                            documents=[text],
                            metadatas=[{"path": path}],
                            embeddings=[vetor.tolist() if hasattr(vetor, "tolist") else vetor]
                        )
                        logger.info(f"Total na coleção após add: {collection.count()}")
                    logger.info(f"✔ Embeddings atualizados para: {path}")
                except Exception as e:
                    logger.error(f"Erro ao processar {path}: {e}")
    if not found:
        logger.warning("Nenhum arquivo .md encontrado!")

def listar_documentos_chromadb(n=5):
    count = collection.count()
    logger.info(f"Total de documentos na coleção: {count}")
    if count == 0:
        logger.warning("Nenhum documento encontrado.")
        return
    results = collection.get(include=['documents', 'metadatas'], limit=n)
    for i, (doc, meta) in enumerate(zip(results['documents'], results['metadatas'])):
        logger.info(f"Documento {i+1}: Caminho: {meta['path']} | Trecho: {doc[:200]}...")