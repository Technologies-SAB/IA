import re
import html

SQL_KEYWORDS = {
    'select', 'from', 'where', 'insert', 'update', 'delete', 'join', 'left join',
    'right join', 'inner join', 'group by', 'order by', 'having', 'create', 'alter',
    'drop', 'table', 'view', 'index', 'procedure', 'begin', 'end', 'case', 'when',
    'then', 'else', 'as', 'on', 'distinct'
}

def _guess_is_sql(code_content: str, threshold: int = 2) -> bool:
    content_lower = code_content.lower()
    score = sum(1 for keyword in SQL_KEYWORDS if keyword in content_lower)
    return score >= threshold

def process_code_blocks_in_markdown(markdown_text: str) -> str:
    code_block_regex = r"```(.*?)?\n(.*?)\n```"
    
    def replacer_func(match):
        language = (match.group(1) or "").strip().lower()
        code_content = match.group(2)
        
        cleaned_content = html.unescape(code_content).strip()
        
        if not language and _guess_is_sql(cleaned_content):
            language = 'sql'
            
        return f"\n```{language}\n{cleaned_content}\n```\n"

    return re.sub(code_block_regex, replacer_func, markdown_text, flags=re.DOTALL)
