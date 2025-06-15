import os
from src.config import settings
from src.utils.save_html import save_html
from src.utils.fetch_json import fetch_json

save_folder = settings.CONFLUENCE_SAVE_FOLDER
space_keys = settings.CONFLUENCE_SPACE_KEY

os.makedirs(save_folder, exist_ok=True)

def download_all_pages(space_key):
    auth = (settings.CONFLUENCE_USERNAME, settings.CONFLUENCE_API_TOKEN)
    base_url = settings.CONFLUENCE_URL

    start = 0
    limit = 500
    pages = []

    while True:
        url = f"{base_url}/rest/api/content?spaceKey={space_key}&limit={limit}&start={start}&expand=body.storage"
        data = fetch_json(url, auth)
        pages.extend(data['results'])
        if 'size' in data and data['size'] < limit:
            break
        start += limit
    return pages

if __name__ == "__main__":
    for space_key in space_keys:
        print(f"🔍 A buscar páginas para o espaço: {space_key}")
        pages = download_all_pages(space_key)
        save_html(pages, space_key, save_folder)
        print(f"✅ {len(pages)} páginas salvas para o espaço {space_key} em {save_folder}/{space_key}")