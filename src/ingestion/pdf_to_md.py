import os
from unstructured.partition.pdf import partition_pdf
from tqdm import tqdm
from config import settings

pdf_to_md_folder = os.path.join(settings.MD_FOLDER, "pdfs")

def convert_pdf_to_md():
    os.makedirs(settings.MD_FOLDER, exist_ok=True)

    space_keys = settings.CONFLUENCE_SPACE_KEY

    for space_key in os.listdir(settings.PDF_DIR):
        space_pdf_folder = os.path.join(settings.PDF_DIR, space_key)

        if not os.path.isdir(space_pdf_folder):
            continue

        pdf_to_md_folder = os.path.join(pdf_to_md_folder, space_key)
        
        os.makedirs(pdf_to_md_folder, exist_ok=True)

        pdf_files = [f for f in os.listdir(space_pdf_folder) if f.endswith(".pdf")]

        for pdf_filename in tqdm(pdf_files, desc=f"Processando {space_key}"):
            pdf_path = os.path.join(space_pdf_folder, pdf_filename)
            md_filename = pdf_filename.replace(".pdf", ".md")
            md_path = os.path.join(pdf_to_md_folder, md_filename)
            
            if os.path.exists(md_path):
                continue

            try:
                elements = partition_pdf(
                    filename=pdf_path,
                    strategy="hi_res",
                    infer_table_structure=True,
                )

                markdown_content = "\n\n".join([el.text for el in elements])

                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

            except Exception as e:
                print(f"Erro ao converter {pdf_filename}: {e}")
    print("✅ Conversão de todos os PDFs para Markdown concluída.")