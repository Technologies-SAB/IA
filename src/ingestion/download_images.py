import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.auth import HTTPBasicAuth
from tqdm import tqdm

from config import settings
from utils.clean_filename import sanitize_filename

ATTACHMENTS_FOLDER = settings.IMAGES_FOLDER
auth = HTTPBasicAuth(settings.CONFLUENCE_USERNAME, settings.CONFLUENCE_API_TOKEN)

def search_attachments(page_id):
    url = f"{settings.CONFLUENCE_URL}/rest/api/content/{page_id}/child/attachment"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()['results']

def download_single_attachment(attachment, space_key):
    page_title = attachment['page_title']
    file_name = sanitize_filename(attachment['title'])
    
    subfolder = os.path.join(ATTACHMENTS_FOLDER, space_key, sanitize_filename(page_title))
    os.makedirs(subfolder, exist_ok=True)
    
    file_path = os.path.join(subfolder, file_name)
    
    download_url = f"{settings.CONFLUENCE_URL}{attachment['_links']['download']}"

    try:
        response = requests.get(download_url, auth=auth, timeout=60)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return f"OK: {file_name}"
    except Exception as e:
        return f"ERRO ao baixar {file_name}: {e}"


def download_attachments_batch(attachments, space_key, max_workers=10):
    """
    Recebe uma lista de anexos e os baixa em paralelo.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_single_attachment, attachment, space_key) for attachment in attachments]
        
        for future in tqdm(as_completed(futures), total=len(attachments), desc=f"Baixando anexos"):
            future.result()