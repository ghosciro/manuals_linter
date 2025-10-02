#ifndef PersonalOutline_H
#define PersonalOutline_H
#include <list>
#include <poppler-qt5.h>
#include <stdexcept>
#include <QString>
using namespace std;
class PersonalOutline{
public:
    PersonalOutline();
    PersonalOutline(QString name);
    static PersonalOutline qt5OutlinerToMine(QVector<Poppler::OutlineItem> outliner);
    void Print_outline();
    ~PersonalOutline();
    QString name;
    list<PersonalOutline> children;
    void add_child(PersonalOutline child);
    void remove_child(int index);
    PersonalOutline get_child(int index);
    int num_children();
private:

};



#endif // PersonalOutline_H