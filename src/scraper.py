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
    fileplace = link.replace("https://dnd5e.wikidot.com","")
    folder=fileplace.split(':')[0]
    filename=fileplace.split(':')[-1]
    os.makedirs(f'pages/{folder}', exist_ok=True)
    filepath = f'pages/{folder}/{filename}.md'
    try:
        html = apri_pagina_html(link)
        soup = BeautifulSoup(html, 'html.parser')
        markdown=""

        containers=soup.find_all(class_=["yui-navset","yui-navset-top"])
        if containers:
            for container in containers:
                title_list=container.find(class_="yui-nav").get_text().strip().split("\n")
                tables=container.find_all(class_="wiki-content-table")
                for i, table in enumerate(tables):
                    title = title_list[i] if i < len(title_list) else f"Table {i+1}"
                    markdown += f"## {title}\n\n"
                    # Convert HTML table to Markdown
                    headers = [th.get_text(strip=True) for th in table.find_all('th')]
                    if headers:
                        markdown += "| " + " | ".join(headers) + " |\n"
                        markdown += "| " + " | ".join(['---'] * len(headers)) + " |\n"
                    rows = table.find_all('tr')
                    for row in rows[1:] if headers else rows:
                        cols = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                        if cols:
                            markdown += "| " + " | ".join(cols) + " |\n"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
    except Exception as e:
        print(f"Errore nel download di {link}: {e}")


if __name__ == "__main__":
        base_url = "https://dnd5e.wikidot.com"
        html = apri_pagina_html(base_url)
        #estrapola tutti i hlink
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')
        links = [base_url+link.get('href') for link in links if link.get('href') and link.get('href').startswith('/')]
        links = list(set(links))  # Rimuovi duplicati
        links=links
        #prima crea una pagina per ogni link

        os.makedirs('pages', exist_ok=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            executor.map(download_and_save, links)
#download_and_save("https://dnd5e.wikidot.com/spells")
# Funzione per aprire una pagina HTML e restituirne il contenuto
