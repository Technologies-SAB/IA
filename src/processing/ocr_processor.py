import pytesseract
from PIL import Image
import os
from tqdm import tqdm
from config import settings

def extract_text_from_images():

    image_folder = settings.IMAGES_FOLDER
    
    image_files = [os.path.join(root, file) for root, _, files in os.walk(image_folder) for file in files if file.lower().endswith(('png', 'jpg', 'jpeg', 'tiff'))]

    for image_path in tqdm(image_files, desc="Processando OCR"):
        text_file_path = f"{image_path}.txt"
        
        if os.path.exists(text_file_path):
            continue
        
        try:
            text = pytesseract.image_to_string(Image.open(image_path), lang='por+eng')
            if text.strip():
                with open(text_file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
        except Exception as e:
            print(f"Erro ao processar OCR para {image_path}: {e}")
    
    print("✅ Processamento de OCR concluído.")