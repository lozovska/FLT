#ifndef StructuresHeader_h
#define StructuresHeader_h

#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include "UsefulFunctionsHeader.h"

struct Derevce{char sym; struct Derevce* r; struct Derevce* l;};
struct Pravila{struct Derevce* before; struct Derevce* after; struct Pravila* next;};
struct Sub{string vars; struct Derevce* tree; struct Sub* next;};

//Строим начальное дерево
struct Derevce* Tree_Make(struct Derevce* d, string str){
    if (d == NULL){
        d = new(struct Derevce);
        d->sym = ' ';
        d->l = d->r = NULL;
    }

    if (str[0] == '('){
        if (str[str.size()-1] == '*'){
            d->sym = '*';
            str.erase(0,1);
            str.erase(str.size()-2);
            d->l=Tree_Make(d->l,str);
        }
        else{
            str.erase(0,1);
            str.erase(str.size()-1);
            if (str[0] == '('){
                int k = 1, i = 0;
                for (i = 1; k && i < str.size(); i++) if (str[i]=='(') k++; else if (str[i]==')') k--;
                if (i == str.size()) d = Tree_Make(d, str);
                else if (str[i] == '|'){
                    d->sym = '|';
                    d->l = Tree_Make(d->l, str.substr(0, i));
                    d->r = Tree_Make(d->r, str.substr(i+1));
                }
                else{
                    int find1 = Iscem_chto_to(str.substr(0,i)), find2 = Iscem_chto_to(str.substr(i));
                    if (find1 == 1 && find2 == 1){
                      d->sym = '+';
                      d->l = Tree_Make(d->l, str.substr(0, i));
                      d->r = Tree_Make(d->r, str.substr(i));
                    }
                    
                    else if (find1 == 1 && find2 == 0) d = Tree_Make(d, str.substr(0, i));
                    else if (find1 == 0 && find2 == 1) d = Tree_Make(d, str.substr(i));
                }
            }
            else if (str.size()){
                if ((str.size() == 1) && ((str[0] >= 'a'&& str[0] <= 'z') || (str[0] >= 'A' && str[0] <= 'Z'))) d->sym = str[0];
                else if (str.size() == 2 && str[str.size()-1] == '*'){
                    d->sym = '*';
                    str.erase(str.size()-1);
                    d->l = Tree_Make(d->l, str);
                }
                else{
                    int i = 0;
                    if (str[1] == '*' && str[2]=='|') i = 2;
                    if (str[1] == '|') i = 1;
                    if ((i == 2) || (i == 1)){
                        d->sym = '|';
                        d->l = Tree_Make(d->l, str.substr(0, i));
                        d->r = Tree_Make(d->r, str.substr(i+1));
                    }
                    else if (str[1] != '*'){
                        int i = Iscem_chto_to(str.substr(1));
                        if (i){
                            d->sym = '+';
                            d->l = Tree_Make(d->l, str.substr(0, 1));
                            d->r = Tree_Make(d->r, str.substr(1));
                        }
                        else d = Tree_Make(d, str.substr(0, 1));
                    }
                    else{
                        int i = Iscem_chto_to(str.substr(2));
                        if (i){
                            d->sym = '+';
                            d->l = Tree_Make(d->l, str.substr(0,2));
                            d->r = Tree_Make(d->r, str.substr(2));
                        }
                        else d = Tree_Make(d, str.substr(0,2));
                    }
                }
            }
        }
    }
    else if ((((str.size()) && (str[0] >= 'a' && str[0] <= 'z')) || (str[0] >= 'A' && str[0] <= 'Z'))){
        if (str[str.size()-1] == '*'){
            d->sym = '*';
            str.erase(str.size()-1);
            d->l = Tree_Make(d->l, str);
        }
        else d->sym = str[0];
    }
    return d;
}

// Чистим деревце :(
struct Derevce* DeleteTree(struct Derevce* d){
    if (d != NULL){
        if (d->l != NULL) d = DeleteTree(d->l);
        if (d->r != NULL) d = DeleteTree(d->r);
        delete(d);
    }
    return d;
}

// Строим новое деревце :)
struct Derevce* New_One(struct Derevce* d,struct Sub* s){
    if (s != NULL && d != NULL){
        if (d->l != NULL){
            if ((d->l->sym >= 'a' && d->l->sym <= 'z') || (d->l->sym >= 'A' && d->l->sym <= 'Z')){
                 if (!Iscem_variables(d->l->sym)){
                    struct Sub* dop = s;
                    string var;
                    var.push_back(d->l->sym);
                    while (dop->next != NULL){
                        if (dop->vars == var) break;
                        else dop = dop->next;
                    }
                    d->l = dop->tree;
                 }
            }
            else d->l = New_One(d->l, s);
        }
        
        if (d->r != NULL){
            if ((d->r->sym >= 'a' && d->r->sym <= 'z') || (d->r->sym >= 'A' && d->r->sym <= 'Z')){
                if (!Iscem_variables(d->r->sym)){
                    struct Sub* dop = s;
                    string var;
                    var.push_back(d->r->sym);
                    while (dop->next != NULL){
                        if (dop->vars == var) break;
                        else dop = dop->next;
                    }
                    d->r = dop->tree;
                }
            }
            else d->r = New_One(d->r, s);
        }
        
        if ((d->l == NULL && d->r == NULL) && ((d->sym >= 'a' && d->sym <= 'z') || (d->sym >= 'A' && d->sym <= 'Z')) && (!Iscem_variables(d->sym))){
            struct Sub* dop = s;
            string var;
            var.push_back(d->sym);
            while (dop->next != NULL){
                if (dop->vars == var) break;
                else dop = dop->next;
            }
            d = dop->tree;
        }
    }
    return d;
}

// Копируем деревце :D
struct Derevce* Copy_Tree(struct Derevce* q,struct Derevce* d){
    if (d != NULL){
        if (q == NULL){q = new(struct Derevce); q->l = q->r = NULL; q->sym = d->sym;}
        if (d->l != NULL) q->l = Copy_Tree(q->l, d->l);
        if (d->r != NULL) q->r = Copy_Tree(q->r, d->r);
    }
   return q;
}

struct Sub* Substitution(struct Sub* p, struct Derevce* regex, struct Derevce* rule){
    if (p == NULL){p = new(struct Sub); p->vars = ' '; p->next = NULL; p->tree = NULL;}
    
    int key = 0;
    for (int i = 0; i < 3; i++) if (rule->sym == operation[i]) key = 1;

    if (key){
        if (rule->sym != regex->sym) return NULL;
        if (rule->l!=NULL) p = Substitution(p, regex->l, rule->l);
        if (p == NULL) return NULL;
        else{
            if ((rule->sym!='*') && (rule->r!=NULL)) p = Substitution(p, regex->r, rule->r);
            if (p == NULL) return NULL;
        }
    }

    else if ((rule->sym >= 'a' && rule->sym <= 'z') || (rule->sym >= 'A' && rule->sym <= 'Z')){
        if (Iscem_variables(rule->sym)){if (rule->sym != regex->sym) return NULL;}
        else {
            if (p->tree==NULL){p->vars = rule->sym; p->tree = regex;}
            else p->next = Substitution(p->next, regex, rule);
        }
    }
    else if (rule->sym!=regex->sym) return NULL;
    return p;
}

struct Sub* Unification(struct Sub* p, struct Sub* q){
    if (p != NULL){
        if (q == NULL){
            if (p->next != NULL) p->next = Unification(p->next, p->next);
        }
        else{
            if (q->next != NULL){
                if (p->vars == q->next->vars){
                    p = Substitution(p, p->tree, q->next->tree);
                    if (p == NULL) return NULL;
                    else q->next = q->next->next;
                }
            }
            p = Unification(p, q->next);
        }
    }
    else p = NULL;
    return p;
}

// Проверяем деревце :)
struct Derevce* Check_Center(int *error, struct Pravila* p, struct Derevce* d){
    if (p != NULL && d != NULL){
        struct Sub* s = NULL;
        s = Substitution(s, d, p->before); s = Unification(s, s);
        if (s != NULL){
            struct Derevce* dop_tree = NULL;
            *error = 1;
            struct Derevce* per = NULL;
            per = Copy_Tree(per, p->after);
            dop_tree = New_One(per, s);
            if (dop_tree != NULL) d = dop_tree;
        }
    }
    return d;
}

struct Derevce* TREE_PASS(int *error, struct Pravila* p, struct Derevce* d){
    if (*error == 0 && p != NULL && d != NULL){
        if (d->l != NULL){
            struct Sub* s = NULL;
            s = Substitution(s, d->l, p->before); s = Unification(s, s);
            if (s != NULL){
                struct Derevce* dop_tree = NULL;
                *error = 1;
                struct Derevce* per = NULL;
                per = Copy_Tree(per, p->after);
                dop_tree = New_One(per, s);
                if (dop_tree != NULL) d->l = dop_tree;
            }
            else d->l = TREE_PASS(error, p, d->l);
        }
         if (*error == 0 && d->r != NULL){
            struct Sub* s = NULL;
            s = Substitution(s, d->r, p->before);
            s = Unification(s, s);
            if (s != NULL){
                struct Derevce* dop_tree = NULL;
                *error = 1;
                struct Derevce* per = NULL;
                per = Copy_Tree(per, p->after);
                dop_tree = New_One(per, s);
                if (dop_tree != NULL) d->r = dop_tree;
            }
            else if (*error == 0) {d->l = TREE_PASS(error, p, d->l); d->r = TREE_PASS(error, p, d->r);}
        }
    }
    return d;
}

// Алгоритм нормализации... 
struct Derevce* Normalization(struct Derevce* d, struct Pravila *p){
    struct Pravila* dop = p;
    int error = 0;
    while (dop != NULL){
        d = Check_Center(&error, dop, d);
        error = 0;
        d = TREE_PASS(&error, dop, d);
        if (error == 1) dop=p;
        else dop = dop->next;
        error = 0;
    }
    return d;
}

struct Pravila* DeleteRules(struct Pravila* t, int i){
    int find = rules[i].find("=");
    string v,f;
    for (char c:rules[i].substr(0,find)) if (c != ' ') v += c;
    string key = v;
    for (char c:rules[i].substr(find+1)) if (c != ' ') f += c;
    string num = f;
    struct Derevce* p = NULL;
    p = Tree_Make(p, key);
    struct Derevce* q = NULL;
    q = Tree_Make(q, num);

    if (t == NULL){t = new(struct Pravila); t->before = p; t->after = q; t->next = NULL;}
    i++;
    if (i < rules.size()) t->next = DeleteRules(t->next, i);
    return t;
}

#endif
