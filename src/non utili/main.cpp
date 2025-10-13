using namespace std;
#include "main.h"


const QString filePath = "/home/dennis/progetti/manuals_linter/resources/manuale.pdf";


int main() {
    Poppler::Document* doc = Poppler::Document::load(filePath);
    if (doc == nullptr) {
        cerr << "Errore nell'apertura del file PDF." << endl;
        return 1;  
    }
    auto outline = doc->outline();
    if (outline.isEmpty()) {
        cout << "Nessun sommario trovato." << endl;
    } 
    else {
        cout << "Sommario trovato:" << endl;
        PersonalOutline personalOutline = PersonalOutline::qt5OutlinerToMine(outline);
        personalOutline.Print_outline();
    }
    delete doc;
    return 0;
}

