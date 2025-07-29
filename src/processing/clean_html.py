from bs4 import BeautifulSoup

def clean_html_boilerplate(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Remove elementos de boilerplate (cabeçalhos, rodapés, menus, etc.) do HTML do Confluence.
    """
    selectors_to_remove = [
        '#main-header',
        '#footer',
        '.page-metadata',
        '.breadcrumbs',
        '#page-navigation',
        '.page-header-actions',
        '#likes-and-labels-container',
        '#comments-section',
        'ac\\:structured-macro[ac\\:name="excerpt"]',
        'ac\\:structured-macro[ac\\:name="contentbylabel"]'
    ]

    for selector in selectors_to_remove:
        for element in soup.select(selector):
            element.decompose()
    return soup