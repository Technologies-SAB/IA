import os
import logging
from bs4 import BeautifulSoup
import html2text
from config import settings
from concurrent.futures import ThreadPoolExecutor

log_folder = "log"
os.makedirs(log_folder, exist_ok=True)

success_logger = logging.getLogger("conversion_success")
error_logger = logging.getLogger("conversion_error")

success_handler = logging.FileHandler(os.path.join(log_folder, "conversion_success.log"))
error_handler = logging.FileHandler(os.path.join(log_folder, "conversion_error.log"))

success_logger.addHandler(success_handler)
error_logger.addHandler(error_handler)

def convert_html_to_md(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    markdown = html2text.html2text(str(soup))
    return markdown

def proccess_html_files(html_folder, md_folder, space_keys):
    try:
        if not os.path.exists(md_folder):
            os.makedirs(md_folder, exist_ok=True)

        for space_key in space_keys:
            html_space_folder = os.path.join(html_folder, space_key)
            md_space_folder = os.path.join(md_folder, space_key)
        if not os.path.exists(md_space_folder):
            os.makedirs(md_space_folder, exist_ok=True)

        if not os.path.exists(html_space_folder):
            print(f"⚠️ Pasta {html_space_folder} não encontrada, pulando...")

        for filename in os.listdir(html_space_folder):
            if filename.endswith('.html'):
                html_path = os.path.join(html_space_folder, filename)
                md_filename = filename.replace('.html', '.md')
                md_path = os.path.join(md_space_folder, md_filename)

                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    
                    markdown = convert_html_to_md(html_content)
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(markdown)
                    logging.info(f"Arquivo convertido com sucesso: {md_path}")
    except Exception as e:
        logging.error(f"Erro ao processar {html_path}: {e}")
