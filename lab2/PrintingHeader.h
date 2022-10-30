#ifndef PrintingHeader_h
#define PrintingHeader_h

#include "StructuresHeader.h"
using namespace std;

void For_Tree(struct Derevce* d){
    if (d->sym == ' ') cout << "$" << endl;
    else cout << d->sym << endl;
    if (d->l != NULL) For_Tree(d->l);
    if (d->r != NULL) For_Tree(d->r);
}

void For_Rules(Pravila* p){
    cout << "KEY: " << endl;
    For_Tree(p->before);
    cout<< endl << "NUM: " << endl;
    For_Tree(p->after);
    cout << endl;
    if (p->next != NULL) For_Rules(p->next);
}

void For_Sub(struct Sub* s){
    if (s != NULL){
        cout<< s->vars << ":" << endl;
        For_Tree(s->tree);
        cout << endl;
        if (s->next != NULL) For_Sub(s->next);
    }
    else cout << "UNIFICATION ПРОПАЛ :(";
}

string For_Expr(string str, struct Derevce* d){
    if (d != NULL){
        if (d->sym == '*'){
            if ((d->l->sym >= 'a' && d->l->sym <= 'z') || (d->l->sym >= 'A' && d->l->sym <= 'Z')){
                str += For_Expr(str, d->l);
                str += '*';
            }
            else{
                string dop_str=str;
                str += '(';
                str += For_Expr(dop_str,d->l);
                str += ')';
                str += '*';
            }
        }
        else if (d->sym == '|'){
            string dop_str = str;
            str += '(';
            str += For_Expr(dop_str, d->l);
            str += '|';
            str += For_Expr(dop_str, d->r);
            str += ')';
        }
        else if (d->sym == '+'){
            string dop_str=str;
            str+='(';
            str+=For_Expr(dop_str,d->l);
            str+=For_Expr(dop_str,d->r);
            str+=')';
        }
        else str += d->sym;
    }
    return str;
}

#endif
