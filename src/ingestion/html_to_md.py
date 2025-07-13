import os
import html2text
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tqdm import tqdm

from config import settings
from utils.clean_filename import clean, sanitize_filename

HTML_FOLDER = settings.CONFLUENCE_SAVE_FOLDER
ATTACHMENTS_FOLDER = settings.IMAGES_FOLDER
MD_FOLDER = settings.MD_FOLDER

def process_and_convert_to_md():
    os.makedirs(MD_FOLDER, exist_ok=True)
    
    skipped_empty_count = 0

    for space_key in os.listdir(HTML_FOLDER):
        html_space_folder = os.path.join(HTML_FOLDER, space_key)
        if not os.path.isdir(html_space_folder): continue

        md_space_folder = os.path.join(MD_FOLDER, space_key)
        os.makedirs(md_space_folder, exist_ok=True)

        html_files = [f for f in os.listdir(html_space_folder) if f.endswith('.html')]

        print(f"\nProcessando HTML do espaço: {space_key}")
        for html_filename in tqdm(html_files, desc=f"Convertendo"):
            page_title_cleaned = os.path.splitext(html_filename)[0]
            html_path = os.path.join(html_space_folder, html_filename)
            md_path = os.path.join(md_space_folder, html_filename.replace('.html', '.md'))

            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            soup = BeautifulSoup(html_content, 'html.parser')
            
            page_text = soup.get_text().strip()
            
            if not page_text:
                skipped_empty_count += 1
                continue

            for img in soup.find_all('img'):
                img_src = img.get('src')
                if not img_src: continue
                
                img_name = os.path.basename(urlparse(img_src).path)
                local_img_folder = os.path.join(ATTACHMENTS_FOLDER, space_key, page_title_cleaned)
                local_img_path = os.path.join(local_img_folder, sanitize_filename(img_name))
                
                if os.path.exists(local_img_path):
                    relative_path = os.path.relpath(local_img_path, start=md_space_folder)
                    img['src'] = relative_path.replace("\\", "/")
                else:
                    img['alt'] = f"{img.get('alt', '')} (Imagem não encontrada localmente: {img_name})"

            h = html2text.HTML2Text()
            h.body_width = 0
            markdown_content = h.handle(str(soup))

            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

    print(f"\n✅ Conversão para Markdown concluída.")
    if skipped_empty_count > 0:
        print(f"ℹ️  {skipped_empty_count} páginas vazias foram ignoradas.")