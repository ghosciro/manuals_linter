#include "personal_outline.h"
using namespace std;

PersonalOutline::PersonalOutline() {
    name = "";
    children = list<PersonalOutline>();
}

PersonalOutline::PersonalOutline(QString name) {
    this->name = name;
    children = list<PersonalOutline>();
}
PersonalOutline::~PersonalOutline() {
    if (children.empty()) return;
    for (auto& child : children) {
        child.~PersonalOutline();
    }
    children.clear();
}

void PersonalOutline::Print_outline() {
}
PersonalOutline PersonalOutline::qt5OutlinerToMine(QVector<Poppler::OutlineItem> outliner){
    PersonalOutline returnOutline;
    for (const auto& item : outliner) {
        returnOutline.add_child(PersonalOutline(item.name()));
        if(item.hasChildren()){
            auto children = item.children();
            returnOutline.get_child(returnOutline.num_children()-1).children = qt5OutlinerToMine(children).children;
        }
    }
    return returnOutline;
}


void PersonalOutline::add_child(PersonalOutline child) {
    children.push_back(child);
}

void PersonalOutline::remove_child(int index) {
    if (index < 0 || index >= children.size()) {
        throw out_of_range("Index out of range");
    }
    auto it = children.begin();
    advance(it, index);
    children.erase(it);
}
PersonalOutline PersonalOutline::get_child(int index) {
    if (index < 0 || index >= children.size()) {
        throw out_of_range("Index out of range");
    }
    auto it = children.begin();
    advance(it, index);
    return *it;
}
int PersonalOutline::num_children() {
    return children.size();
}
