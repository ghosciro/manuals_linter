import os
from concurrent.futures import ThreadPoolExecutor
import re

IMPORTANT_WORDS=[]

def linker(text):
    for word in IMPORTANT_WORDS:
        pattern = r'\b' + re.escape(word) + r'\b'
        text = re.sub(pattern, f'[[{word}]]', text, flags=re.IGNORECASE)
    return text

if __name__ == "__main__":
    cartelle=os.listdir('pages')
    for cartella in cartelle:
        IMPORTANT_WORDS.append(cartella.lower())
        for file in os.listdir(f'pages/{cartella}'):
            IMPORTANT_WORDS.append(file.replace('.md','').lower())
        
    for cartella in cartelle:
        for file in os.listdir(f'pages/{cartella}'):
            def process_file(cartella, file):
                with open(f'pages/{cartella}/{file}', 'r') as f:
                    content = f.read()
                    linked_content = linker(content)
                with open(f'pages/{cartella}/{file}', 'w') as f:
                    f.write(linked_content)

            with ThreadPoolExecutor() as executor:
                executor.submit(process_file, cartella, file)


    print(IMPORTANT_WORDS)