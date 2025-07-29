import os
import html
from bs4 import BeautifulSoup
import html2text
from tqdm import tqdm
from urllib.parse import urlparse, unquote

from config import settings

from processing.clean_html import clean_html_boilerplate
from processing.code_processor import process_code_blocks_in_markdown

from processing.clean_markdown import clean_markdown_file 
from utils.clean_filename import sanitize_filename

HTML_FOLDER = settings.CONFLUENCE_SAVE_FOLDER
ATTACHMENTS_FOLDER = settings.IMAGES_FOLDER
MD_FOLDER = settings.MD_FOLDER


def pre_process_confluence_macros(soup: BeautifulSoup):
    code_macros = soup.select('ac\\:structured-macro[ac\\:name="code"]')
    for macro in code_macros:
        lang_param = macro.find('ac:parameter', {'ac:name': 'language'})
        language = lang_param.get_text().strip() if lang_param else ''
        body = macro.find('ac:plain-text-body')
        if not body: continue
        
        code_text = body.get_text(strip=True)
        new_pre_tag = soup.new_tag("pre")
        new_code_tag = soup.new_tag("code")
        if language:
            new_code_tag['class'] = f"language-{language}"
        new_code_tag.string = code_text
        new_pre_tag.append(new_code_tag)
        macro.replace_with(new_pre_tag)
    return soup


def handle_drawio_images(soup: BeautifulSoup, page_title_cleaned: str, space_key: str, md_space_folder: str):
    drawio_macros = soup.select('ac\\:structured-macro[ac\\:name="drawio"]')
    for macro in drawio_macros:
        diagram_name_param = macro.find('ac:parameter', {'ac:name': 'diagramName'})
        if not diagram_name_param: continue
        
        img_filename = sanitize_filename(diagram_name_param.get_text())
        display_name_param = macro.find('ac:parameter', {'ac:name': 'diagramDisplayName'})
        alt_text = display_name_param.get_text() if display_name_param else img_filename
        
        local_img_folder = os.path.join(ATTACHMENTS_FOLDER, space_key, page_title_cleaned)
        local_img_path = os.path.join(local_img_folder, img_filename)
        
        new_img_tag = soup.new_tag("img")
        if os.path.exists(local_img_path):
            relative_path = os.path.relpath(local_img_path, start=md_space_folder)
            new_img_tag['src'] = relative_path.replace("\\", "/")
            new_img_tag['alt'] = alt_text
        else:
            new_img_tag['src'] = ""
            new_img_tag['alt'] = f"IMAGEM DRAWIO NÃO ENCONTRADA: {img_filename}"
        macro.replace_with(new_img_tag)
    return soup


def process_and_convert_to_md():
    os.makedirs(MD_FOLDER, exist_ok=True)
    
    all_html_files = []
    for space_key in os.listdir(HTML_FOLDER):
        html_space_folder = os.path.join(HTML_FOLDER, space_key)
        if not os.path.isdir(html_space_folder): continue
        for html_filename in os.listdir(html_space_folder):
            if html_filename.endswith('.html'):
                all_html_files.append((space_key, html_filename))

    if not all_html_files:
        print("Nenhum arquivo HTML encontrado para converter.")
        return

    print(f"\n--- Iniciando Conversão de {len(all_html_files)} arquivos HTML para Markdown ---")
    
    for space_key, html_filename in tqdm(all_html_files, desc="Convertendo HTML -> MD"):
        
        page_title_cleaned = os.path.splitext(html_filename)[0]

        html_path = os.path.join(HTML_FOLDER, space_key, html_filename)
        md_space_folder = os.path.join(MD_FOLDER, space_key)
        os.makedirs(md_space_folder, exist_ok=True)
        md_path = os.path.join(md_space_folder, html_filename.replace('.html', '.md'))

        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        soup = clean_html_boilerplate(soup)
        
        soup = pre_process_confluence_macros(soup)
        soup = handle_drawio_images(soup, page_title_cleaned, space_key, md_space_folder)
        
        h = html2text.HTML2Text(bodywidth=0)
        markdown_content = h.handle(str(soup))
        
        processed_md = process_code_blocks_in_markdown(markdown_content)
        final_markdown = clean_markdown_file(processed_md)
        
        if not final_markdown.strip():
            continue

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(final_markdown)

    print("\n✅ Conversão para Markdown concluída.")