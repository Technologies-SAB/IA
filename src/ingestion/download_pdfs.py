import os
import requests
from requests.auth import HTTPBasicAuth
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from config import settings
from utils.clean_filename import clean
from utils.fetch_json import fetch_json

PDF_SAVE_FOLDER = "data/pdfs"

def download_all_pages_meta(space_key):
    """
    Busca apenas os metadados (ID e título) de todas as páginas em um espaço.
    """
    auth = (settings.CONFLUENCE_USERNAME, settings.CONFLUENCE_API_TOKEN)
    base_url = settings.CONFLUENCE_URL
    start = 0
    limit = 100
    pages_meta = []
    
    print(f"Buscando metadados das páginas para o espaço '{space_key}'...")
    while True:
        url = f"{base_url}/rest/api/content?spaceKey={space_key}&limit={limit}&start={start}"
        data = fetch_json(url, auth)
        results = data.get('results', [])
        
        if not results:
            break
        
        pages_meta.extend(results)
        if len(results) < limit:
            break
        start += len(results)
    
    print(f"Encontrados {len(pages_meta)} páginas no espaço '{space_key}'.")
    return pages_meta

def download_pdf_for_page(page_meta, space_key, auth):
    """
    Baixa uma única página como PDF.
    """
    page_id = page_meta['id']
    title = clean(page_meta['title'])
    
    pdf_export_url = f"{settings.CONFLUENCE_URL}/exportword?pageId={page_id}"

    space_folder = os.path.join(PDF_SAVE_FOLDER, space_key)
    os.makedirs(space_folder, exist_ok=True)
    pdf_path = os.path.join(space_folder, f"{title}.pdf")

    if os.path.exists(pdf_path):
        return f"EXISTE: {title}.pdf"

    try:
        response = requests.get(pdf_export_url, auth=auth, timeout=120) # Timeout maior para PDFs
        response.raise_for_status()

        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        return f"OK: {title}.pdf"
    except requests.exceptions.RequestException as e:
        return f"ERRO ao baixar {title}.pdf: {e}"

def download_confluence_pdfs():
    auth = (settings.CONFLUENCE_USERNAME, settings.CONFLUENCE_API_TOKEN)
    os.makedirs(PDF_SAVE_FOLDER, exist_ok=True)

    for space_key in settings.CONFLUENCE_SPACE_KEY:
        pages_to_download = download_all_pages_meta(space_key)

        if not pages_to_download:
            print(f"Nenhuma página encontrada para o espaço {space_key}.")
            continue
        
        print(f"Iniciando download de {len(pages_to_download)} PDFs para o espaço '{space_key}'...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(download_pdf_for_page, page, space_key, auth): page for page in pages_to_download}
            
            for future in tqdm(as_completed(futures), total=len(pages_to_download), desc=f"Baixando PDFs de {space_key}"):
                result = future.result()
                if "ERRO" in result or "EXISTE" in result:
                    pass
        print(f"✅ Download de PDFs para o espaço {space_key} concluído.")