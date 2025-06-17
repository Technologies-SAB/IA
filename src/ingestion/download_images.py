import os
import requests
from requests.auth import HTTPBasicAuth
from src.utils.fetch_json import fetch_json
from src.config import settings
from src.utils.clean_filename import sanitize_filename

image_folder = settings.CONFLUENCE_IMAGES_FOLDER

if not os.path.exists(image_folder):
    os.makedirs(image_folder, exist_ok=True)

auth = HTTPBasicAuth(settings.CONFLUENCE_USERNAME, settings.CONFLUENCE_API_TOKEN)

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

def dowload_archive(attachment, space_key):
    file_name = sanitize_filename(attachment['title'])
    file_url = attachment['_links']['download']
    file_path = os.path.join(image_folder, space_key, file_name)

    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    response = requests.get(f"{settings.CONFLUENCE_URL}{file_url}", auth=auth)
    response.raise_for_status()

    with open(file_path, 'wb') as f:
        f.write(response.content)
    
    print(f"✅ Imagem {file_name} baixada com sucesso em {file_path}")