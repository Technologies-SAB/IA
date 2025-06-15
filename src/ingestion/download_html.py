import os
import re
import requests
from src.config import settings
from src.utils.save_html import save_pages

save_folder = settings.CONFLUENCE_SAVE_FOLDER

os.makedirs(save_folder, exist_ok=True)

def download_all_pages():
    import requests
    from src.utils import fetch_json

    auth = (settings.CONFLUENCE_USERNAME, settings.CONFLUENCE_API_TOKEN)
    base_url = settings.CONFLUENCE_BASE_URL

    start = 0
    limit = 500

    while True:
        url = f"{base_url}/rest/api/content?spaceKey={settings.CONFLUENCE_SPACE_KEY}&limit={limit}&start={start}&expand=body.storage"
        data = fetch_json(url, auth)
        pages.extend(data['results'])
        if 'size' in data and data['size'] < limit:
            break
        start += limit
    return pages

def __init__():
    for space_key in space_keys:
        global pages
        pages = download_all_pages()
        save_pages(pages, settings.CONFLUENCE_SPACE_KEY)