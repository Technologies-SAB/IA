import faiss
import pickle
import os
import numpy as np
import logging
from sentence_transformers import SentenceTransformer
from config import settings

logger = logging.getLogger(__name__)

class FaissRetriever:
    def __init__(self):
        self.index_path = os.path.join(settings.EMBEDDINGS_DIR, 'faiss.index')
        self.metadata_path = os.path.join(settings.EMBEDDINGS_DIR, 'faiss_metadatas.pkl')
        
        if not os.path.exists(self.index_path) or not os.path.exists(self.metadata_path):
            raise FileNotFoundError("Índice FAISS ou metadados não encontrados. Execute generate_embeddings.py primeiro.")

        logger.info("Carregando índice FAISS e metadados...")
        self.index = faiss.read_index(self.index_path)
        with open(self.metadata_path, 'rb') as f:
            self.metadatas = pickle.load(f)
        
        logger.info("Carregando modelo de embedding para queries...")
        model_path = os.path.join(settings.MODEL_DIR_BASE, settings.MODEL_NAME)
        self.model = SentenceTransformer(model_path)
        
        logger.info(f"Retriever pronto. {self.index.ntotal} vetores carregados.")

    def search(self, query: str, top_k: int = 5):
        """
        Busca os chunks de texto mais similares à query.
        """
        logger.debug(f"Buscando por: '{query}' com top_k={top_k}")
        
        # 1. Gerar o embedding da query
        query_vec = self.model.encode([query]).astype('float32')
        
        # 2. Buscar no FAISS
        distances, indices = self.index.search(query_vec, top_k)
        
        # 3. Montar os resultados com o texto dos chunks
        resultados = []
        for idx, dist in zip(indices[0], distances[0]):
            # FAISS pode retornar -1 se não encontrar vizinhos suficientes
            if idx != -1:
                metadata = self.metadatas[idx]
                resultados.append({
                    'text': metadata['text'],
                    'source': metadata['source'],
                    'distance': float(dist)
                })
        
        logger.debug(f"Encontrados {len(resultados)} resultados.")
        return resultados

# Exemplo de uso (pode ser executado para testar)
if __name__ == '__main__':
    try:
        retriever = FaissRetriever()
        query = "Qual o procedimento para check-in?"
        resultados = retriever.search(query, top_k=3)
        
        print(f"Resultados da busca para: '{query}'\n")
        for res in resultados:
            print(f"--- Fonte: {res['source']} ---")
            print(res['text'])
            print(f"(Distância: {res['distance']:.4f})\n")
            
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        print("Certifique-se de executar o script `generate_embeddings.py` primeiro.")