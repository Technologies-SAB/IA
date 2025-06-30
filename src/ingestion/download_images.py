import logging
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.auth import HTTPBasicAuth

from utils.fetch_json import fetch_json
from config import settings
from utils.clean_filename import sanitize_filename

image_folder = settings.CONFLUENCE_IMAGES_FOLDER

if not os.path.exists(image_folder):
    os.makedirs(image_folder, exist_ok=True)

auth = HTTPBasicAuth(settings.CONFLUENCE_USERNAME, settings.CONFLUENCE_API_TOKEN)

log_folder = "log"
os.makedirs(log_folder, exist_ok=True)

logging.basicConfig(level=logging.INFO)
success_logger = logging.getLogger("success")
error_logger = logging.getLogger("error")
timeout_logger = logging.getLogger("timeout")

success_handler = logging.FileHandler(os.path.join(log_folder, "download_success.log"))
error_handler = logging.FileHandler(os.path.join(log_folder, "download_error.log"))
timeout_handler = logging.FileHandler(os.path.join(log_folder, "download_timeout.log"))

success_logger.addHandler(success_handler)
error_logger.addHandler(error_handler)
timeout_logger.addHandler(timeout_handler)

def listing_spaces(space_key):
    start = 0
    limit = 10000
    pages = []

    while True:
        url = f"{settings.CONFLUENCE_URL}/rest/api/content?spaceKey={space_key}&limit={limit}&start={start}&expand=title"
        print(f"🔍 A buscar imagens para o espaço: {space_key}")

        data = fetch_json(url, auth)
        pages.extend(data['results'])
        if 'size' in data and data['size'] < limit:
            break
        start += limit 
    response = requests.get(url, auth=auth)
    response.raise_for_status()

    return response.json()['results']

def search_attachments(page_id):
    url = f"{settings.CONFLUENCE_URL}/rest/api/content/{page_id}/child/attachment?expand=metadata"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()['results']

def dowload_archive(attachment, space_key, page_title):
    file_name = sanitize_filename(attachment['title'])
    subfolder = os.path.join(image_folder, space_key, sanitize_filename(page_title))

    if not os.path.exists(subfolder):
        os.makedirs(subfolder, exist_ok=True)

    file_path = os.path.join(subfolder, file_name)
    
    file_url = attachment['_links']['download']

    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    response = requests.get(f"{settings.CONFLUENCE_URL}{file_url}", auth=auth, timeout=60)
    response.raise_for_status()

    with open(file_path, 'wb') as f:
        f.write(response.content)

def download_attachments_batch(attachments, space_key, page_title, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(dowload_archive, attachment, space_key, page_title)
            for attachment in attachments
        ]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                error_logger.error(f"Erro ao baixar anexo: {e}")