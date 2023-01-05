import os
from collections import Counter

def append_dot(a):
    jj = a.replace("->", "->.")
    return jj

def closure(a):
    temp = [a]
    for it in temp:
        jj = it[it.index(".") + 1]
        if jj != len(it) - 1:
            for k in prod:
                if k[0][0] == jj and (append_dot(k)) not in temp:
                    temp.append(append_dot(k))
        else:
            for k in prod:
                if k[0][0] == jj and it not in temp:
                    temp.append(it)
    return temp

def swap(new, pos):
    new = list(new)
    temp = new[pos]
    if pos != len(new):
        new[pos] = new[pos + 1]
        new[pos + 1] = temp
        new1 = "".join(new)
        return new1
    else:
        return "".join(new)

def goto1(x1):
    hh = []
    pos = x1.index(".")
    if pos != len(x1) - 1:
        jj = list(x1)
        kk = swap(jj, pos)
        if kk.index(".") != len(kk) - 1:
            jjj = closure(kk)
            return jjj
        else:
            hh.append(kk)
            return hh
    else:
        return x1

def get_list(graph, state):
    final = []
    for g in graph:
        if int(g.split()[0]) == state:
            final.append(g)

    return final

if __name__ == '__main__':
    prod = []
    set_of_items = []
    c = []

    with open("test3.txt", 'r') as fp:
        for i in fp.readlines():
            prod.append(i.strip())

    prod.insert(0, "X->S")
    #print("Augmented Grammar")
    #print(prod)

    prod_num = {}
    for i in range(1, len(prod)):
        prod_num[str(prod[i])] = i

    j = closure("X->.S")
    set_of_items.append(j)

    state_numbers = {}
    dfa_prod = {}
    items = 0
    while True:
        if len(set_of_items) == 0:
            break

        jk = set_of_items.pop(0)
        kl = jk
        c.append(jk)
        state_numbers[str(jk)] = items
        items += 1

        if len(jk) > 1 or (jk[0][-1] != '.'):
            for item in jk:
                jl = goto1(item)
                if jl not in set_of_items and jl != kl:
                    set_of_items.append(jl)
                    dfa_prod[str(state_numbers[str(jk)]) + " " + str(item)] = jl
                else:
                    dfa_prod[str(state_numbers[str(jk)]) + " " + str(item)] = jl

    for item in c:
        for j in range(len(item)):
            if goto1(item[j]) not in c:
                #print(goto1(item[j]))
                if item[j].index(".") != len(item[j]) - 1:
                    c.append(goto1(item[j]))

    length = len(c)
    #print("Total States: ", length)
    endings = {}
    for i in range(len(c)):
        #print(i, ":", c[i])
        if (i != 1) & (len(c[i]) == 1) & (c[i][0].endswith('.')) : endings[i] = c[i][0]

    dfa = {}
    for i in range(length):
        if i in dfa:
            pass
        else:
            lst = get_list(dfa_prod, i)
            samp = {}
            for j in lst:
                s = j.split()[1].split('->')[1]
                search = s[s.index('.') + 1]
                samp[search] = state_numbers[str(dfa_prod[j])]

            if samp != {}:
                dfa[i] = samp

    # Вывод в dot
    #print(dfa)
    with open("lr0.gv.txt", "w") as f:
        sss = 'digraph finite_state_machine {\n\tfontname="Helvetica,Arial,sans-serif"\n\tnode [fontname="Helvetica,Arial,sans-serif"]\n\tedge [fontname="Helvetica,Arial,sans-serif"]\n\trankdir=LR;\n\tnode [shape = Mrecord];\n'
        for i in range(len(c)):
            st = f"STATE {str(i)} \\n"
            for i1, s in enumerate(c[i]):
                if i1 == (len(c[i]) - 1):
                    st += f"{s}"
                else:
                    st += f"{s}\\n"
            sss += f'\t"{i}" [label = "{st}"]'.replace("->", "-\>") + "\n"

        for i in dfa.keys():
            for k, v in dfa[i].items():
                sss += (f'\t{i} -> {v} [label = "{k}"];\n')
        sss += '}'
        f.write(sss)
    os.system('dot -Gsize=10,15 -Tpng lr0.gv.txt > lr0.png')

    # ---------------- Преобразование в PDA ---------------------------
    new_dfa = {}
    for i, j in dfa.items():
        for k, l in j.items():
            if l == 1: dfa[i][k] = [l, '0/#']
            else: dfa[i][k] = [l, '#/'+ str(l) + '#']

    epsilon_transitions = {}
    svertka_po = {}
    for i, j in endings.items():
        l = len((j.strip('.').split('->'))[1]) - 1
        svertka_po[i] = (j.strip('.').split('->'))[0]
        transit = {}
        transit[i] = [length, str(i) + '/$']
        length += 1
        key = i

        # добавляем эпсилон-переходы
        for k in range(l):
            for a, b in dfa.items():
                for e, d in b.items():
                    if d[0] == key:
                        key = a
                        transit[length-1] = [length, str(key) + '/$']
                        length += 1
                        break

        epsilon_transitions[i] = transit

    # добавляем новые переходы из послееднего состояния, в которое перешли по эпсилон
    new_transitions = {}
    for i, j in epsilon_transitions.items():
        last_one = list(j.keys())[-1]
        s = str(svertka_po[i]) + '.'
        transit = {}
        transit[svertka_po[i]] = []
        for a, b in enumerate(c):
            for d, e in enumerate(b):
                if e.find(s) != -1:
                    key = a
                    for g, h in dfa.items():
                        for o, p in h.items():
                            if p[0] == key:
                                key = g
                    if a == 1:
                        transit[svertka_po[i]].append([a, '0/ '])
                    else:
                        transit[svertka_po[i]].append([a, str(key) + '/' + str(a) + ' ' + str(key)])
        new_transitions[j[last_one][0]] = {svertka_po[i] : transit[svertka_po[i]]}

    # избавляемся от "бесполезных" состояний
    for i, j in endings.items():
        for a, b in dfa.items():
            for d, e in b.items():
                if e[0] == i:
                    dfa[a][d] = [epsilon_transitions[i][i][0], '#/#']
        for a, b in new_transitions.items():
            for d, e in b.items():
                for v, t in enumerate(e):
                    if t[0] == i:
                        print()
                        new_transitions[a][d][v] = [epsilon_transitions[i][i][0], t[1].replace(str(i), '#')]

    # удаление переходов по нетерминалам
    flags = {}
    for i, j in dfa.items():
        for a, b in j.items():
            if a.isupper(): flags[i] = a

    for i, j in flags.items():
        dfa[i].pop(j)

    # Соединяем все словари
    # к dfa прибавляем epsilon
    flags = []
    for i, j in epsilon_transitions.items():
        j.pop(i)
        if len(j) == 0: flags.append(i)

    for i in flags: epsilon_transitions.pop(i)

    for i, j in epsilon_transitions.items():
        for a, b in j.items():
            dfa[a] = {'ε' : b}
    helppp = len(dfa)

    # к dfa прибавляем new
    for i, j in new_transitions.items():
        key = list(j.keys())[0]
        dfa[i] = {'ε' : j[key]}

    # выводим в dot
    with open("pda.gv.txt", "w") as f:
        sss = 'digraph finite_state_machine {\n\tfontname="Helvetica,Arial,sans-serif"\n\tnode [fontname="Helvetica,Arial,sans-serif"]\n\tedge [fontname="Helvetica,Arial,sans-serif"]\n\trankdir=LR;\n\t node [shape = doublecircle]; 1;\n\t node [shape = circle];\n'

        for i, j in enumerate(dfa.keys()):
            for k, v in dfa[j].items():
                if i < helppp:
                    sss += (f'\t{j} -> {v[0]} [label = "{k},{v[1]}"];\n')
                else:
                    for a in v:
                        sss += (f'\t{j} -> {a[0]} [label = "{k},{a[1]}"];\n')
        sss += '}'
        f.write(sss)
    os.system('dot -Gsize=10,15 -Tpng pda.gv.txt > pda.png')