from bs4 import BeautifulSoup

def clean_html_boilerplate(soup: BeautifulSoup) -> BeautifulSoup:
    selectors_to_remove = [
        '#main-header', '#footer', '.page-metadata', '.breadcrumbs',
        '#page-navigation', '.page-header-actions', '#likes-and-labels-container',
        '#comments-section',
        'ac\\:structured-macro[ac\\:name="excerpt"]',
        'ac\\:structured-macro[ac\\:name="contentbylabel"]'
    ]
    
    for selector in selectors_to_remove:
        for element in soup.select(selector):
            element.decompose()

    metadata_table_headers = ["Document Classification", "Document Revision History"]
    for table in soup.find_all("table"):
        header_text = table.get_text().strip()
        if any(h in header_text for h in metadata_table_headers):
            if table.find("h2"):
                continue
            table.decompose()
            
    return soup