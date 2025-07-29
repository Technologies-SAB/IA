import re

def clean_markdown_file(markdown_text: str) -> str:
    """Aplica uma série de limpezas a um texto em formato Markdown."""
    
    processed_text = markdown_text
    
    processed_text = re.sub(r'\n{3,}', '\n\n', processed_text)
    
    processed_text = re.sub(r'!\[\]\(\s*\)', '', processed_text)
    
    lines = processed_text.split('\n')
    cleaned_lines = [line for line in lines if line.strip() != '']
    processed_text = '\n'.join(cleaned_lines)
    
    return processed_text.strip()