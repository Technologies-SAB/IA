import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from bs4 import BeautifulSoup
from config import settings
from utils.save_html import save_html
from utils.fetch_json import fetch_json
from utils.clean_filename import clean
from ingestion.download_images import search_attachments, download_attachments_batch

HTML_SAVE_FOLDER = settings.CONFLUENCE_SAVE_FOLDER
ATTACHMENTS_FOLDER = settings.IMAGES_FOLDER
SPACE_KEYS = settings.CONFLUENCE_SPACE_KEY

OBSOLETE_KEYWORDS = [
    "outdated",
    "check new article",
    "obsolete",
    "obsoleto",
    "consulte o novo artigo",
    "desatualizado",
    "deprecated",
    "(outdated)",
    "antigo",
    "legacy",
    "v9",
    "v 9",
    "v9.0",
    "v 9.0",
    "v9.1",
    "v 9.1",
    "v9.2",
    "v 9.2",
    "v9.3",
    "v 9.3",
    "v9.4",
    "v 9.4",
    "v9.5",
    "v 9.5",
    "v9.6",
    "v 9.6",
    "v9.7",
    "v 9.7",
    "v9.8",
    "v 9.8",
    "v9.9",
    "v 9.9",
    "não utilizar",
    "não usar"
]

def is_page_obsolete(page: dict) -> bool:
    """
    Verifica se uma página é obsoleta, checando tanto o título quanto o conteúdo.
    Recebe o objeto 'page' completo da API do Confluence.
    Retorna True se a página for obsoleta, False caso contrário.
    """
    title = page.get('title', '').lower()
    for keyword in OBSOLETE_KEYWORDS:
        if keyword in title:
            return True 
        
    html_content = page.get('body', {}).get('storage', {}).get('value', '')
    if not html_content:
        return False 
        
    soup = BeautifulSoup(html_content, 'html.parser')
    page_text = soup.get_text().lower()
    
    for keyword in OBSOLETE_KEYWORDS:
        if keyword in page_text:
            return True
            
    return False


def download_all_pages(space_key):
    auth = (settings.CONFLUENCE_USERNAME, settings.CONFLUENCE_API_TOKEN)
    base_url = settings.CONFLUENCE_URL
    start = 0
    limit = 100
    pages = []
    
    print(f"Buscando metadados das páginas para o espaço '{space_key}'...")
    with tqdm(desc="Buscando páginas", unit=" págs") as pbar:
        while True:
            url = f"{base_url}/rest/api/content?spaceKey={space_key}&limit={limit}&start={start}&expand=body.storage"
            data = fetch_json(url, auth)
            results = data.get('results', [])
            
            if not results:
                break
            
            pages.extend(results)
            pbar.update(len(results))
            if len(results) < limit:
                break
            start += len(results)
            
    print(f"Encontradas {len(pages)} páginas no total no espaço '{space_key}'.")
    return pages

def download_all_attachments_for_space(pages, space_key):
    print(f"\nBuscando todos os anexos para as páginas válidas do espaço '{space_key}'...")
    all_attachments_to_download = []
    
    for page in tqdm(pages, desc=f"Verificando anexos de {space_key}"):
        page_id = page['id']
        page_title = clean(page['title'])
        
        try:
            attachments = search_attachments(page_id)
            for attachment in attachments:
                attachment['page_title'] = page_title
                
                file_name = clean(attachment['title'])
                subfolder = os.path.join(ATTACHMENTS_FOLDER, space_key, clean(page_title))
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
    """
    Função principal que orquestra o download, com a nova lógica de filtragem combinada.
    """
    os.makedirs(HTML_SAVE_FOLDER, exist_ok=True)
    os.makedirs(ATTACHMENTS_FOLDER, exist_ok=True)
    
    for space_key in SPACE_KEYS:
        print(f"\n--- Processando espaço: {space_key} ---")
        
        all_pages = download_all_pages(space_key)
        if not all_pages:
            print(f"⚠️ Nenhuma página encontrada para o espaço {space_key}.")
            continue
            
        print("Filtrando páginas obsoletas (título e conteúdo)...")
        valid_pages = []
        obsolete_count = 0
        for page in all_pages:
            if is_page_obsolete(page):
                obsolete_count += 1
            else:
                valid_pages.append(page)
        
        print(f"Filtragem concluída. {len(valid_pages)} páginas válidas, {obsolete_count} páginas obsoletas ignoradas.")

        if not valid_pages:
            print(f"Nenhuma página válida restou após a filtragem para o espaço {space_key}.")
            continue

        save_html(valid_pages, space_key, HTML_SAVE_FOLDER)
        print(f"✅ {len(valid_pages)} páginas HTML salvas para o espaço {space_key}.")
        
        download_all_attachments_for_space(valid_pages, space_key)