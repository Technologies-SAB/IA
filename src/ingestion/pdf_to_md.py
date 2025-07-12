import os
from unstructured.partition.pdf import partition_pdf
from tqdm import tqdm
from config import settings

def convert_pdf_to_md():
    os.makedirs(settings.MD_FOLDER, exist_ok=True)

    space_keys = settings.CONFLUENCE_SPACE_KEY

    for space_key in os.listdir(settings.PDF_DIR):
        space_pdf_folder = os.path.join(settings.PDF_DIR, space_key)

        if not os.path.isdir(space_pdf_folder):
            continue

        