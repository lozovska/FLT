#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include "StructuresHeader.h"
#include "PrintingHeader.h"
#include "UsefulFunctionsHeader.h"

using namespace std;

struct Pravila* pravila = NULL;
struct Derevce* regex_derevce = NULL;
int error = 0;

int main(){
    ifstream in("test7.txt");
    getline(in, regex);
    if (!regex.size()) error = 1;
    
    string str;
    while (getline(in, str)){
        if (str.size()) rules.push_back(str);
    }
    
    if (error){
        cout << "ERROR :(";
        return 0;
    }
    
    pravila = DeleteRules(pravila, 0);
    
    string v;
    for (char c:regex) if (c != ' ') v += c;
    regex = v;
    
    int key = 0;
    for (int i = 0; i < regex.size(); i++){
        if ((regex[i] >= 'a' && regex[i] <= 'z') || (regex[i] >= 'A' && regex[i] <= 'Z')){
            for (int j = 0; j < variables.size(); j++){
                if (variables[j] == regex[i]){
                    key = 1;
                    break;
                }
            
            }
            if (!key) variables.push_back(regex[i]);
        }
        key = 0;
    }

    regex_derevce = Tree_Make(regex_derevce, regex);
    // Нормализуем деревце
    regex_derevce = Normalization(regex_derevce, pravila);
    // Выводим деревце - ответ :D
    // For_Tree(regex_derevce);
    // Выводим выражение- ответ
    string ans = "";
    ans = For_Expr(ans, regex_derevce);
    cout << ans << endl;
}
