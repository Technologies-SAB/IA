import os
import logging
from tqdm import tqdm
from utils.clean_filename import clean

log_folder = "log"
os.makedirs(log_folder, exist_ok=True)

success_logger = logging.getLogger("save_html_success")
error_logger = logging.getLogger("save_html_error")

success_handler = logging.FileHandler(os.path.join(log_folder, "save_html_success.log"))
error_handler = logging.FileHandler(os.path.join(log_folder, "save_html_error.log"))

success_logger.addHandler(success_handler)
error_logger.addHandler(error_handler)

def save_html(pages, space_key, save_folder):
    
    for page in tqdm(pages, desc=f"Salvando paginas do espaço {space_key}"):
        title = clean(page['title'])
        body_html = page['body']['storage']['value']

        page_folder = os.path.join(save_folder, space_key)
        os.makedirs(page_folder, exist_ok=True)

        try:
            with open(f"{page_folder}/{title}.html", "w", encoding="utf-8") as f:
                f.write(body_html)
            success_logger.info(f"Página {title}.html salva com sucesso.")
        except Exception as e:
            error_logger.error(f"Erro ao salvar {title}.html: {e}")