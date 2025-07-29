import os
import re
import numpy as np
import logging
import pickle
import faiss

from sentence_transformers import SentenceTransformer
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from config import settings
from tqdm import tqdm

logging.basicConfig(
    filename='embeddings.log',
    filemode='w', 
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

FAISS_INDEX_PATH = os.path.join(settings.EMBEDDINGS_DIR, 'faiss.index')
FAISS_METADATA_PATH = os.path.join(settings.EMBEDDINGS_DIR, 'faiss_metadatas.pkl')

def inject_ocr_text_into_markdown(markdown_text: str, md_file_path: str) -> str:
    """
    Percorre um texto Markdown, encontra referências de imagens e injeta o texto OCR
    correspondente diretamente no corpo do texto.
    
    Args:
        markdown_text: O conteúdo completo do arquivo .md.
        md_file_path: O caminho para o arquivo .md, usado para resolver caminhos relativos de imagem.

    Returns:
        O texto markdown com o conteúdo dos textos OCR injetados.
    """

    image_regex = r'!\[(.*?)\]\((.*?)\)'

    matches = list(re.finditer(image_regex, markdown_text))

    for match in reversed(matches):
        alt_text = match.group(1)
        image_relative_path = match.group(2)
        
        base_dir = os.path.dirname(md_file_path)
        ocr_text_path = os.path.normpath(os.path.join(base_dir, image_relative_path + '.txt'))
        
        ocr_content = ""
        if os.path.exists(ocr_text_path):
            try:
                with open(ocr_text_path, 'r', encoding='utf-8') as f:
                    ocr_content = f.read().strip()
            except Exception as e:
                logger.warning(f"Não foi possível ler o arquivo OCR {ocr_text_path}: {e}")

        if ocr_content:
            replacement_text = (
                f"\n\n--- INÍCIO DO CONTEÚDO DA IMAGEM: {alt_text} ---\n"
                f"{ocr_content}\n"
                f"--- FIM DO CONTEÚDO DA IMAGEM ---\n\n"
            )
            
            start, end = match.span()
            markdown_text = markdown_text[:start] + replacement_text + markdown_text[end:]

    return markdown_text


def create_smart_chunks(full_text: str, source_path: str):
    headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
    md_header_splits = markdown_splitter.split_text(full_text)
    
    recursive_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    final_chunks = recursive_splitter.split_documents(md_header_splits)

    chunks_with_metadata = []
    for i, chunk in enumerate(final_chunks):
        metadata = {
            "source": source_path,
            "chunk_id": i,
            "text": chunk.page_content,
            **chunk.metadata
        }
        chunks_with_metadata.append(metadata)

    return chunks_with_metadata

def load_embedding_model():
    logger.info(f"Carregando modelo de embedding: {settings.MODEL_NAME}")
    model_path = os.path.join(settings.MODEL_DIR_BASE, settings.MODEL_NAME)
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo de embeddings não encontrado em {model_path}. Execute 'python src/main.py models' primeiro.")
    model = SentenceTransformer(model_path)
    logger.info("Modelo de embedding carregado com sucesso.")
    return model

def update_embedding(md_directory):
    try:
        model = load_embedding_model()
    except FileNotFoundError as e:
        logger.error(e)
        print(f"ERRO: {e}")
        return

    all_chunks_with_metadata = []
    os.makedirs(settings.EMBEDDINGS_DIR, exist_ok=True)
    logger.info(f"Iniciando varredura de arquivos .md em: {md_directory}")
    
    all_files = [os.path.join(root, file) for root, _, files in os.walk(md_directory) for file in files if file.endswith(".md")]
    if not all_files:
        logger.warning("Nenhum arquivo .md encontrado!")
        return

    print(f"Processando {len(all_files)} arquivos Markdown para gerar embeddings...")
    for path in tqdm(all_files, desc="Gerando Embeddings"):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                full_text = f.read()
            
            logger.info(f"Injetando texto OCR para o arquivo: {path}")
            enriched_text = inject_ocr_text_into_markdown(full_text, path)
            
            chunks_data = create_smart_chunks(enriched_text, path)

            if not chunks_data:
                logger.warning(f"Nenhum chunk de texto gerado para: {path}")
                continue

            all_chunks_with_metadata.extend(chunks_data)
            logger.info(f"✔ {len(chunks_data)} chunks (incluindo OCR) gerados para: {path}")

        except Exception as e:
            logger.error(f"Erro ao processar {path}: {e}")
    
    if not all_chunks_with_metadata:
        logger.warning("Nenhum embedding foi gerado.")
        return

    texts_to_embed = [chunk['text'] for chunk in all_chunks_with_metadata]
    metadatas = all_chunks_with_metadata

    print(f"\nGerando embeddings para {len(texts_to_embed)} chunks de texto...")
    embeddings = model.encode(texts_to_embed, show_progress_bar=True)
    
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