import fitz  # PyMuPDF
from fitz import Document
import os
FILES_PATH="resources/manuale.pdf"
RESULTS_PATH="results"

import os
class pdf_extractor:
    def __init__(self, pdf_path=FILES_PATH,results_path=RESULTS_PATH):
        self.pdf_path = pdf_path
        self.results_path = results_path
        self.document = fitz.open(pdf_path)
        self.outlines = self.cluttering(self.document.get_toc()) # type: ignore

    def cluttering(self,outlines):
        """
        Build a nested dictionary representing the hierarchy of titles in a table of contents.

        Parameters
        ----------
        toc_list : list of tuple
            A list of tuples (level, title, page_number), where:
            - level : int, heading level
            - title : str, heading title
            - page_number : int, page number of the heading

        Returns
        -------
        dict
            Nested dictionary: top-level titles as keys, second-level titles as keys in nested dicts,
            values are tuples (start_page, end_page)
        """
        clutters={}
        temp_title=""
        for element in outlines:
            if element[0]==1:
                clutters[element[1]]={}
                temp_title=element[1]
            if element[0]==2:
                clutters[temp_title][element[1]]=element[2]
        last_page_number=self.document.page_count
        for element in clutters.keys().__reversed__():
            for subelement in clutters[element].keys().__reversed__():
                clutters[element][subelement]=last_page_number,clutters[element][subelement]
                last_page_number=clutters[element][subelement][1]
        return clutters
    def make_dirs(self,path=None):
        if path is None:
            path=self.results_path
        '''
        makes directories for results if they do not exist
        Creates a main results directory and subdirectories for each top-level title in the outlines.
        Each subdirectory is named after the title, with spaces replaced by underscores.

        Parameters
        ----------
        path : str
            The main directory path where subdirectories will be created.
        Returns
        -------
        None
        ---------------------------------------------------------------------------
        
        '''
        if not os.path.exists(path):
            os.makedirs(path)
        for element in self.outlines.keys():
            dir_name = f"{path}/{element.replace(' ', '_')}"
            print(dir_name)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)           

    def make_files(self,results_path=None):
        if results_path is None:
            results_path=self.results_path
        '''
        Creates markdown files for each second-level title in the outlines.
        Each file is named after the title, with spaces replaced by underscores, and is placed in the corresponding subdirectory.
        Each file contains the title, page range, and text content from the specified pages in the PDF document.
        Parameters
        ----------
        None
        Returns
        -------
        None
        ---------------------------------------------------------------------------
        '''
        for element in self.outlines.keys():
            for subelement in self.outlines[element].keys():
                file_name=f"{results_path}/{element.replace(' ', '_')}/{subelement.replace(' ', '_')}.md"
                print(file_name)
                with open(file_name, 'w') as f:
                    f.write(f"# {subelement}\n\n")
                    f.write(f"page:{self.outlines[element][subelement]}\n\n")
                    for page_number in range(self.outlines[element][subelement][1],self.outlines[element][subelement][0]-1):
                        page = self.document.load_page(page_number)
                        f.write(f"## Page {page_number+1}\n\n")
                        for block in page.get_text("dict")["blocks"]:
                            if block["type"] != 0:  # solo testo
                                continue
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    text = span["text"]
                                    text = "".join([char for char in text if char.isalpha() or char.isnumeric() or " " in char ]) # rimuovi caratteri non ASCII
                                    size = span["size"]  # dimensione del font
                                    if len(text)>1:  # salta stringhe vuote
                                        if size >= 20:  # titolo principale
                                            f.write(f"\n\n# {text}\n\n")
                                        elif 15 <= size < 20:  # sottotitolo
                                            f.write(f"\n## {text}\n")
                                        elif 14 <= size < 15 or text.isupper():  # sottotitolo minore
                                            f.write(f"\n#### {text}\n")
                                        else:  # testo normale
                                            f.write(f"{text}")

                f.close()

if __name__ == "__main__":
    extractor = pdf_extractor(FILES_PATH,RESULTS_PATH)
    extractor.make_dirs()
    extractor.make_files()