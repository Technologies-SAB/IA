import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from config import settings
from utils.save_html import save_html
from utils.fetch_json import fetch_json
from utils.clean_filename import clean, sanitize_filename
from ingestion.download_images import search_attachments, download_attachments_batch

HTML_SAVE_FOLDER = settings.CONFLUENCE_SAVE_FOLDER
ATTACHMENTS_FOLDER = settings.IMAGES_FOLDER # Vamos tratar tudo como anexo
SPACE_KEYS = settings.CONFLUENCE_SPACE_KEY

def download_all_pages(space_key):
    auth = (settings.CONFLUENCE_USERNAME, settings.CONFLUENCE_API_TOKEN)
    base_url = settings.CONFLUENCE_URL
    start = 0
    limit = 100
    pages = []
    
    print(f"Buscando metadados das páginas para o espaço '{space_key}'...")
    while True:
        url = f"{base_url}/rest/api/content?spaceKey={space_key}&limit={limit}&start={start}&expand=body.storage"
        data = fetch_json(url, auth)
        results = data.get('results', [])
        
        if not results: break
        
        pages.extend(results)
        if len(results) < limit: break
        start += len(results)
        
    print(f"Encontradas {len(pages)} páginas no espaço '{space_key}'.")
    return pages

def download_all_attachments_for_space(pages, space_key):
    print(f"\nBuscando todos os anexos para o espaço '{space_key}'...")
    all_attachments_to_download = []
    
    for page in tqdm(pages, desc=f"Verificando anexos de {space_key}"):
        page_id = page['id']
        page_title = clean(page['title'])
        
        try:
            attachments = search_attachments(page_id)
            for attachment in attachments:
                attachment['page_title'] = page_title
                
                file_name = sanitize_filename(attachment['title'])
                subfolder = os.path.join(ATTACHMENTS_FOLDER, space_key, sanitize_filename(page_title))
                file_path = os.path.join(subfolder, file_name)
                
                if not os.path.exists(file_path):
                    all_attachments_to_download.append(attachment)
        except Exception as e:
            print(f"Erro ao buscar anexos para a página '{page_title}': {e}")
            
    if not all_attachments_to_download:
        print(f"✅ Todos os anexos para o espaço '{space_key}' já estão baixados.")
        return

    print(f"\nBaixando {len(all_attachments_to_download)} novos anexos para o espaço '{space_key}'...")
    download_attachments_batch(all_attachments_to_download, space_key)


def download_confluence_content():
    os.makedirs(HTML_SAVE_FOLDER, exist_ok=True)
    os.makedirs(ATTACHMENTS_FOLDER, exist_ok=True)
    
    for space_key in SPACE_KEYS:
        print(f"\n--- Processando espaço: {space_key} ---")
        
        pages = download_all_pages(space_key)
        if not pages:
            print(f"⚠️ Nenhuma página encontrada para o espaço {space_key}.")
            continue
        
        save_html(pages, space_key, HTML_SAVE_FOLDER)
        print(f"✅ {len(pages)} páginas HTML salvas para o espaço {space_key}.")
        
        download_all_attachments_for_space(pages, space_key)