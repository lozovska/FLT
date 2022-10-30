#ifndef UsefulFunctionsHeader_h
#define UsefulFunctionsHeader_h

#include "StructuresHeader.h"

using namespace std;
vector <string> rules;
vector <char> variables;
string regex;
char operation[3] = {'*', '|', '+'};

int Iscem_chto_to(string s){
    for (int i = 0; i < s.size(); i++){
        if ((s[i] >= 'a' && s[i] <= 'z') || (s[i] >= 'A' && s[i] <= 'Z') || (s[i] == '|'))
            return 1;
    }
    return 0;
}

int Iscem_variables(char sym){
    for (int i = 0; i < variables.size(); i++) if (variables[i] == sym) return 1;
    return 0;
}

#endif
