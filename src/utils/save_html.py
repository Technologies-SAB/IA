import os
from tqdm import tqdm
from src.utils.clean_filename import clean

def save_html(pages, space_key, save_folder):
    
    for page in tqdm(pages, desc=f"Salvando paginas do espaço {space_key}"):
        title = clean(page['title'])
        body_html = page['body']['storage']['value']

        page_folder = os.path.join(save_folder, space_key)
        os.makedirs(page_folder, exist_ok=True)

        with open(f"{page_folder}/{title}.html", "w", encoding="utf-8") as f:
            f.write(body_html)