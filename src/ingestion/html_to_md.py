import os
from bs4 import BeautifulSoup
import html2text
from src.config import settings

def convert_html_to_md(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    markdown = html2text.html2text(str(soup))
    return markdown

def proccess_html_files(html_folder, md_folder):
    if not os.path.exists(md_folder):
        os.makedirs(md_folder, exist_ok=True)

    for filename in os.listdir(html_folder):
        if filename.endswith('.html'):
            html_path = os.path.join(html_folder, filename)
            md_filename = filename.replace('.html', '.md')
            md_path = os.path.join(md_folder, md_filename)

            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            markdown_content = convert_html_to_md(html_content)

            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            print(f"✅ {filename} convertido para Markdown e salvo em {md_path}")