import fitz  # PyMuPDF
from fitz import Document
import os
FILES_PATH="resources/manuale.pdf"
RESULTS_PATH="results"

import os
class pdf_extractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.document = fitz.open(pdf_path)
        self.outlines = self.cluttering(self.document.get_toc())
        self.make_dirs()
        self.make_files()
    def cluttering(self,outlines):
        temp_clutters={}
        temp_title=""
        for element in outlines:
            if element[0]==1:
                temp_clutters[element[1]]={}
                temp_title=element[1]
            if element[0]==2:
                temp_clutters[temp_title][element[1]]=element[2]
        clutters={}
        for key in temp_clutters.keys():
            if len(temp_clutters[key])>1:
                clutters[key]=temp_clutters[key]
        last_page_number=self.document.page_count
        for element in clutters.keys().__reversed__():
            for subelement in clutters[element].keys().__reversed__():
                clutters[element][subelement]=last_page_number,clutters[element][subelement]
                last_page_number=clutters[element][subelement][1]
        return clutters
    def make_dirs(self):
        if not os.path.exists(RESULTS_PATH):
            os.makedirs(RESULTS_PATH)
        for element in self.outlines.keys():
            dir_name = f"{RESULTS_PATH}/{element.replace(' ', '_')}"
            print(dir_name)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)           

    def make_files(self):
        for element in self.outlines.keys():
            for subelement in self.outlines[element].keys():
                file_name=f"{RESULTS_PATH}/{element.replace(' ', '_')}/{subelement.replace(' ', '_')}.md"
                print(file_name)
                with open(file_name, 'w') as f:
                    f.write(f"# {subelement}\n\n")
                    f.write(f"page:{self.outlines[element][subelement]}\n\n")
                    for page_number in range(self.outlines[element][subelement][1],self.outlines[element][subelement][0]-1):
                        page = self.document.load_page(page_number)
                        #text = page.get_text("dict")["blocks"]

                        for block in page.get_text("dict")["blocks"]:
                            if "lines" not in block:
                                continue
                            for line in block["lines"]:
                                if "spans" not in line:
                                    continue
                                for span in line["spans"]:
                                    # Controlla se il flag indica grassetto
                                    # Il bit 0x14 (20 decimale) indica bold nella maggior parte dei PDF
                                    if span["flags"] & 20:
                                        f.write(span["text"] + " ")               
                f.close()
if __name__ == "__main__":
    pdf_path = FILES_PATH
    extractor = pdf_extractor(pdf_path)
