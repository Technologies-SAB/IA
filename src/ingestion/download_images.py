import os
import requests
from requests.auth import HTTPBasicAuth
from src.utils.fetch_json import fetch_json
from src.config import settings

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

