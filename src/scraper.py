import requests
from bs4 import BeautifulSoup
import os
import concurrent.futures

def apri_pagina_html(url):
    response = requests.get(url)
    response.raise_for_status()  # Solleva un'eccezione se la richiesta fallisce
    return response.text

# Esempio d'uso:
# html = apri_pagina_html("https://www.example.com")
# print(html)


def download_and_save(link):
    url = base_url + str(link)
    fileplace = link.strip('/').replace('/', '')
    folder=fileplace.split(':')[0]
    filename=fileplace.split(':')[-1]
    os.makedirs(f'pages/{folder}', exist_ok=True)
    filepath = f'pages/{folder}/{filename}.md'
    try:
        html = apri_pagina_html(url)

        #cerca se ci sono href nel file
        


        soup = BeautifulSoup(html, 'html.parser')
        # Estrai tutte le tabelle
        tables=[]
        for table in soup.find_all('table'):
              table_title=
              # Rimuovi la tabella dal contenuto

        # Semplice conversione in markdown: titoli,paragrafi,liste e tabelle
        markdown = ""
        for element in soup.body.descendants:
            if element.name == 'h1':
                markdown += f"# {element.get_text(strip=True)}\n\n"
            elif element.name == 'h2':
                markdown += f"## {element.get_text(strip=True)}\n\n"
            elif element.name == 'h3':
                markdown += f"### {element.get_text(strip=True)}\n\n"
            elif element.name == 'ul':
                for li in element.find_all('li', recursive=False):
                    markdown += f"- {li.get_text(strip=True)}\n"
                markdown += "\n"
            elif element.name == 'ol':
                for idx, li in enumerate(element.find_all('li', recursive=False), 1):
                    markdown += f"{idx}. {li.get_text(strip=True)}\n"
                markdown += "\n"
            elif element.name == 'table':
                rows = element.find_all('tr')
                for i, row in enumerate(rows):
                    cols = [col.get_text(strip=True) for col in row.find_all(['th', 'td'])]
                    markdown += "| " + " | ".join(cols) + " |\n"
                    if i == 0:
                        markdown += "| " + " | ".join(['---'] * len(cols)) + " |\n"
                markdown += "\n"
            elif element.name == 'p':
                markdown += f"{element.get_text(strip=True)}\n\n"

        #remove Create a Page part
        markdown= markdown.split("Create a Page")[:1]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
    except Exception as e:
        print(f"Errore nel download di {url}: {e}")


if __name__ == "__main__":
    base_url = "https://dnd5e.wikidot.com"
    html = apri_pagina_html(base_url)
    #estrapola tutti i hlink
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    links = [link.get('href') for link in links if link.get('href') and link.get('href').startswith('/')]
    links = list(set(links))  # Rimuovi duplicati
    links=links
    #prima crea una pagina per ogni link

    os.makedirs('pages', exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        executor.map(download_and_save, links)

# Funzione per aprire una pagina HTML e restituirne il contenuto
