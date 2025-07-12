import os
from config import settings
from utils.save_html import save_html
from utils.fetch_json import fetch_json
from ingestion.html_to_md import proccess_html_files
from ingestion.download_images import listing_spaces, search_attachments, dowload_archive, download_attachments_batch

save_folder = settings.CONFLUENCE_SAVE_FOLDER
md_folder = settings.MD_FOLDER
space_keys = settings.CONFLUENCE_SPACE_KEY

os.makedirs(save_folder, exist_ok=True)

def download_all_pages(space_key):
    auth = (settings.CONFLUENCE_USERNAME, settings.CONFLUENCE_API_TOKEN)
    base_url = settings.CONFLUENCE_URL

    start = 0
    limit = 100
    pages = []
    
    print(f"Iniciando download paginado para o espaço '{space_key}'...")

    while True:
        url = f"{base_url}/rest/api/content?spaceKey={space_key}&limit={limit}&start={start}&expand=body.storage"
        print(f"Buscando páginas: start={start}, limit={limit}")
        
        data = fetch_json(url, auth)
        results = data.get('results', [])
        
        if not results:
            print("Nenhuma página adicional encontrada. Finalizando busca.")
            break
        
        pages.extend(results)
        num_results = len(results)
        print(f"Recebidas {num_results} páginas. Total acumulado: {len(pages)}")

        if num_results < limit:
            print("Esta foi a última página de resultados.")
            break

        start += num_results
    
    print(f"Download concluído. Total de {len(pages)} páginas baixadas para o espaço '{space_key}'.")
    return pages

def download_confluence_pages():
    from utils.clean_filename import clean

    for space_key in space_keys:
        print(f"🔍 A buscar páginas para o espaço: {space_key}")
        pages = download_all_pages(space_key)
        
        if not pages:
            print(f"⚠️ Nenhuma página encontrada para o espaço {space_key}.")
            continue

        new_pages = []
        for page in pages:
            title = clean(page['title'])
            page_folder = os.path.join(save_folder, space_key)
            os.makedirs(page_folder, exist_ok=True)
            file_path = os.path.join(page_folder, f"{title}.html")
            if not os.path.exists(file_path):
                new_pages.append(page)

        if new_pages:
            save_html(new_pages, space_key, save_folder)
            print(f"✅ {len(new_pages)} novas páginas salvas para o espaço {space_key} em {save_folder}/{space_key}")
        else:
            print(f"✅ Todas as páginas do espaço {space_key} já estão salvas.")

        spaces = listing_spaces(space_key)
        for space in spaces:
            space_id = space['id']
            space_title = space['title']
            attachments = search_attachments(space_id)

            from utils.clean_filename import sanitize_filename
            from ingestion.download_images import image_folder
            filtered_attachments = []
            for attachment in attachments:
                file_name = sanitize_filename(attachment['title'])
                subfolder = os.path.join(image_folder, space_key, sanitize_filename(space_title))
                file_path = os.path.join(subfolder, file_name)
                if not os.path.exists(file_path):
                    filtered_attachments.append(attachment)

            if filtered_attachments:
                download_attachments_batch(filtered_attachments, space_key, space_title)
            else:
                continue

        if new_pages:
            proccess_html_files(save_folder, md_folder, [space_key])
            print(f"✅ Arquivos HTML processados e convertidos para Markdown em {md_folder}/{space_key}")
        else:
            print(f"✅ Todos os arquivos HTML do espaço {space_key} já foram convertidos.")

