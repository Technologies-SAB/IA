import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions
from src.config import settings

chroma_client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_DIR,
)

collection = chroma_client.get_or_create_collection(
    name="confluence_embeddings"
)

embeder = embedding_functions.SentenceTransformerEmbeddingFunction(settings.MODEL_NAME)

def update_embedding(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    vetor = embeder(text)
                    collection.add(
                        documents=[text],
                        metadatas=[{"path": path}],
                        embeddings=[vetor]
                    )
                print(f"✔ Embeddings atualizados para: {path}")

