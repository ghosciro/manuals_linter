import requests
from urllib.parse import urljoin


from bs4 import BeautifulSoup
from bs4 import Tag
import os
import concurrent.futures
from bs4.element import PageElement
def apri_pagina_html(url):
    response = requests.get(url)
    response.raise_for_status()  # Solleva un'eccezione se la richiesta fallisce
    return response.text
base_url = "http://dnd5e.wikidot.com"
def table_to_markdown(html):
    markdown=""
    if not ( "wiki-content-table" in html.get('class', [])):
        return ""
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        rows = html.find_all('tr')
        futures = []
        links_to_download = []
        for row in rows:
            columns = row.find_all(['th', 'td'])
            column_text = []
            links_text = []

            if row.find('th'):
                # Header row
                header_cells = [cols.get_text(strip=True) for cols in columns]
                markdown += "| " + " | ".join(header_cells) + " |\n"
                markdown += "|" + "|".join(["---"] * len(columns)) + "|\n"
                continue
            else:
                # Data rows
                row_cells = []
                for cols in columns:
                    cell_content = []
                    link_tags = cols.find_all('a')
                    
                    if link_tags:
                        for link in link_tags:
                            link_url = urljoin(base_url, link.get('href'))
                            links_to_download.append(link_url)
                            cell_content.append(f"[[{link.get_text(strip=True)}]]")
                    else:
                        cell_content.append(cols.get_text(strip=True))
                    
                    row_cells.append(" ".join(cell_content))
                
                if row_cells:
                    markdown += "| " + " | ".join(row_cells) + " |\n"
        
        # Submit download tasks
        for link_url in links_to_download:
            futures.append(executor.submit(download_and_save, link_url))
        # Optionally wait for all downloads to finish
        concurrent.futures.wait(futures)
    markdown += "\n"
    return markdown
# Esempio d'uso:
# html = apri_pagina_html("https://www.example.com")
# print(html)

def FormatterMarkdown(child):
    markdown = ""
    if "feature" in (child.get("class") or []):
        for subchild in child.find_all(recursive=False):
            if isinstance(subchild, Tag):
                if yui_navset := subchild.find(class_="yui-navset"):
                    markdown += FormatterMarkdown(yui_navset)
                elif text := subchild.find(class_="col-lg-12"):
                    for text_child in text.find_all(recursive=False):
                        if isinstance(text_child, Tag):
                            markdown += FormatterMarkdown(text_child)
    if child.name == "p":
        markdown += f"{child.get_text().strip()}\n\n"
    elif child.name == "h2":
        title = child.get_text().strip()
        markdown += f"## {title}\n\n"
    elif child.name == "h3":
        title = child.get_text().strip()
        markdown += f"### {title}\n\n"
    elif child.name == "ul":
        for li in child.find_all("li"):
            markdown += f"- {li.get_text().strip()}\n"
        markdown += "\n"
    elif "page-title" in child.get('class', []):
        title = child.get_text().strip()
        markdown += f"# {title}\n\n"
    elif "wiki-content-table" in child.get('class', []):
        markdown += table_to_markdown(child)
    elif "yui-navset" in (child.get("class") or []) or "yui-navset-top" in (child.get("class") or []):
        title_list=child.find(class_="yui-nav").get_text().strip().split("\n")
        tables=child.find_all(class_="wiki-content-table")
        for i, table in enumerate(tables):
            title = title_list[i] if i < len(title_list) else f"Table {i+1}"
            markdown += f"## {title}\n\n"
            markdown += table_to_markdown(table)
            markdown +="\n\n"
            # Convert HTML table to Markdown ,
# Feature sections (the big div with nested content)
    return markdown


def download_and_save(link):
    fileplace = link.replace("http://dnd5e.wikidot.com/","")
    folder=fileplace.split(':')[0].title()
    filename=fileplace.split(':')[-1].strip().replace('/',' ').replace("'","").split("(")[0].replace("-"," ").title()
    os.makedirs(f'pages/{folder}', exist_ok=True)
    filepath = f'pages/{folder}/{filename}.md'
    if os.path.exists(filepath):
        print(f"File {filepath} already exists, skipping download.")
        return
    try:
        print(f"Salvando in {filepath}")
        html = apri_pagina_html(link)
        soup = BeautifulSoup(html, 'html.parser')
        # First find the main content area
        main_content = soup.find(id="page-content")
        with open(filepath, 'w', encoding='utf-8') as f:
            if main_content is not None and isinstance(main_content, Tag):
                for child in main_content.find_all(recursive=False):
                    f.write(FormatterMarkdown(child))
            else:
                print(f"Main content not found or not a Tag for {link}")
    except Exception as e:
        print(f"Errore nel download di {link}: {e}")
        pass

if __name__ == "__main__":
            os.makedirs('pages', exist_ok=True)
            home_page = apri_pagina_html("http://dnd5e.wikidot.com")
            soup = BeautifulSoup(home_page, 'html.parser')
            useful_div = soup.find(id="page-content")
            links = useful_div.find_all('a')
            links = {urljoin(base_url,link.get('href')) for link in links if link.get('href')}
            print(f"Trovati {len(links)} link unici.")
            # Scarica e salva le pagine in parallelo
            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
               executor.map(download_and_save, links)
            #download_and_save("http://dnd5e.wikidot.com/artificer:infusions")
# Funzione per aprire una pagina HTML e restituirne il contenuto
