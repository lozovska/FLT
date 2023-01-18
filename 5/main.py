import json
import os
from tabulate import tabulate
import latextable
from texttable import Texttable

cols_names = [' ','Parent', 'Child', 'MAX', 'MIN']
data = []

def check_names(name):
  flag = 0
  for n in Entities:
    if n.Name == name:
      flag = 1
      return flag
  return flag

def get_key(d, value):
  for i, v in d.items():
    for b in v:
      if b == value:
        return i

class Entity:
  def __init__(self, Name):
    self.Name = Name
    self.PK = []
    self.FK = []
    self.Attributes = []
    self.Parent = {}
    self.Child = {}
    self.OtherRelations = {}


def Parse(x):
  # Имя сущности
  x = x.split('::')
  for i, y in enumerate(x):
    x[i] = x[i].strip(' ').split(';')
  Ent = Entity(x[0][0])

  # Primary Key
  for y in (x[1][0].split(",")):
    Ent.PK.append(y.strip(' '))

  # Foreign Key
  for y in (x[1][1].split(',')):
    if y.find('NULL') != -1: break
    Ent.FK.append(y.strip(' '))

  # Attributes
  for y in (x[1][2].split(',')):
    Ent.Attributes.append(y.strip(' '))

  # Parent
  for y in (x[1][3].replace('Parent : ', '').split(',')):
    if y.find('NULL') != -1: break
    y = y.strip(' ').replace('(', '').replace(')', '')
    Ent.Parent[(y.split(' '))[0]] = (y.split(' '))[1]

  # Сhild
  for y in (x[1][4].replace('Child : ', '').split(',')):
    if y.find('NULL') != -1: break
    y = y.strip(' ').replace('(', '').replace(')', '')
    Ent.Child[(y.split(' '))[0]] = (y.split(' '))[1]

  # Other Relations
  for y in (x[1][5].replace(' OtherRelations : ', '').split(',')):
    if y.find('NULL') != -1: break
    y = y.strip(' ').replace('(', '').replace(')', '')
    Ent.OtherRelations[(y.split(' '))[0]] = (y.split(' '))[1]

  return Ent

def to_json_file(Entities, T):
  dic = {}

  # Заполняем инофрмацию об аттрибутах сущностей
  dic['tables'] = {}
  for d in Entities:
    if d.Name not in dic['tables'].keys():
      dic['tables'][d.Name] = {}
      if T == 2:
        for pk in d.PK:
          dic['tables'][d.Name]["*" + pk] = " "
        for fk in d.FK:
          dic['tables'][d.Name]["+" + fk] = " "
        for at in d.Attributes:
          dic['tables'][d.Name][at] = " "
      else:
        for pk in d.PK:
          dic['tables'][d.Name][pk] = " "
        for fk in d.FK:
          dic['tables'][d.Name][fk] = " "
        for at in d.Attributes:
          dic['tables'][d.Name][at] = " "

  # Заполняем информацию об отношениях между сущностями
  # Сначала преобразовываем обозначение кардинальности к нужному виду
  # 0-M -> *
  # 1-M -> +
  # 1 -> 1

  for j, i in enumerate(Entities):
    for k, v in i.OtherRelations.items():
      if v == "1-M": Entities[j].OtherRelations[k] = "+"
      elif v == "0-M": Entities[j].OtherRelations[k] = "*"

  for j, i in enumerate(Entities):
    for k, v in i.Parent.items():
      if v == "1-M": Entities[j].Parent[k] = "+"
      elif v == "0-M": Entities[j].Parent[k] = "*"

  for j, i in enumerate(Entities):
    for k, v in i.Child.items():
      if v == "1-M": Entities[j].Child[k] = "+"
      elif v == "0-M": Entities[j].Child[k] = "*"

  dic['relations'] = []

  for num, ent in enumerate(Entities):
    for k, v in ent.Parent.items():
      for i in Entities:
        if i.Name == k:
          for k1, v1 in i.Child.items():
            if k1 == ent.Name:
              result = v1
              dic['relations'].append(str(k) + ":" + i.PK[0] + " " + str(v) + "--" + str(result) + " " + ent.Name + ":" + ent.FK[0])
              break

    for k, v in ent.OtherRelations.items():
      for num1, i in enumerate(Entities):
        if (i.Name == k) & (num1 > num):
          for k1, v1 in i.OtherRelations.items():
            if k1 == ent.Name:
              result = v1
              dic['relations'].append(ent.Name + ":" + ent.PK[0] + " " + result + "--" + v + " " + k + ":" + i.PK[0])
              break

  dic["rankAdjustments"] = ""
  dic["label"] = ""
  return dic

if __name__ == '__main__':
  Entities = []
  test = open('test1.txt', 'r').read().splitlines()
  for i, x in enumerate(test):
    Entities.append(Parse(x))

  # Доп задание - построение таблицы кардинальности
  for num, ent in enumerate(Entities):
    for k, v in ent.Parent.items():
      newdata = []
      for i in Entities:
        if i.Name == k:
          for k1, v1 in i.Child.items():
            if k1 == ent.Name:
              newdata.append(k)               # Parent
              newdata.append(ent.Name)        # Child
              # MAX и MIN
              if i.Child[ent.Name] == '1':
                if ent.Parent[i.Name] == '1':
                  newdata.append('1:1')
                  newdata.append('M-O')
                if ent.Parent[i.Name] == '0-M':
                  newdata.append('1:N')
                  newdata.append('M-O')
                if ent.Parent[i.Name] == '1-M':
                  newdata.append('N:1')
                  newdata.append('M-M')
              if i.Child[ent.Name] == '0-M':
                if ent.Parent[i.Name] == '1':
                  newdata.append('N:1')
                  newdata.append('O-M')
                if ent.Parent[i.Name] == '0-M':
                  newdata.append('M:N')
                  newdata.append('O-O')
                if ent.Parent[i.Name] == '1-M':
                  newdata.append('M:N')
                  newdata.append('O-M')
              if i.Child[ent.Name] == '1-M':
                if ent.Parent[i.Name] == '1':
                  newdata.append('1:N')
                  newdata.append('M-M')
                if ent.Parent[i.Name] == '0-M':
                  newdata.append('M:N')
                  newdata.append('M-O')
                if ent.Parent[i.Name] == '1-M':
                  newdata.append('M:N')
                  newdata.append('M-M')
              data.append(newdata)
              break

    for k, v in ent.OtherRelations.items():
      newdata = []
      for num1, i in enumerate(Entities):
        if (i.Name == k) & (num1 > num):
          for k1, v1 in i.OtherRelations.items():
            if k1 == ent.Name:
              print('------------')
              print(ent.Name, i.Name)
              newdata.append(ent.Name)               # Parent
              newdata.append(i.Name)                # Child
              if i.OtherRelations[ent.Name] == '1':
                if ent.OtherRelations[i.Name] == '1':
                  newdata.append('1:1')
                  newdata.append('M-O')
                if ent.OtherRelations[i.Name] == '0-M':
                  newdata.append('1:N')
                  newdata.append('M-O')
                if ent.OtherRelations[i.Name] == '1-M':
                  newdata.append('1:N')
                  newdata.append('M-M')
              if i.OtherRelations[ent.Name] == '0-M':
                if ent.OtherRelations[i.Name] == '1':
                  newdata.append('1:N')
                  newdata.append('O-M')
                if ent.OtherRelations[i.Name] == '0-M':
                  newdata.append('M:N')
                  newdata.append('O-O')
                if ent.OtherRelations[i.Name] == '1-M':
                  newdata.append('M:N')
                  newdata.append('O-M')
              if i.OtherRelations[ent.Name] == '1-M':
                if ent.OtherRelations[i.Name] == '1':
                  newdata.append('1:N')
                  newdata.append('M-M')
                if ent.OtherRelations[i.Name] == '0-M':
                  newdata.append('M:N')
                  newdata.append('M-O')
                if ent.OtherRelations[i.Name] == '1-M':
                  newdata.append('M:N')
                  newdata.append('M-M')
              data.append(newdata)
              break
 
  # Латееееееех таблица
  table = Texttable()
  table.set_cols_align(["l", "r", "c", "c"])
  table.set_deco(Texttable.HEADER | Texttable.VLINES)
  table.add_rows(data)
  print('Latex Table')
  print(latextable.draw_latex(table, caption="Cardinality"))

  # Модель сущность-связь
  dic = to_json_file(Entities, 1)
  with open("diagram1.json", "w") as write_file:
    json.dump(dic, write_file, indent=4)
  command = "python3 --version"

  os.system("erdot diagram1.json")
  os.system("dot diagram1.dot -Tpng -o diagram1.png")

  # Преобразование в реляционную модель
  # Отличием от ER-модели является обозначения PK и FK
  # А также для связи многие ко многим создается новая сущность

  # Проверим на связь многие ко многим
  pattern = ['*--*', '+--*', '*--+', '+--+']
  for x in dic['relations']:
    for y in pattern:
      if x.find(y) != -1:
        z = x.split(' '+y+' ')
        z1 = z[0].split(':')
        z2 = z[1].split(':')
        
        # тут коллизия - учу новые русские слова:)
        if check_names(z1[0] + '_by_' + z2[0]) == 0 :
          ent = Entity(z1[0] + '_by_' + z2[0])
        else:
          for i in range(1000):
            if check_names(z1[0] + '_by_' + z2[0] + str(i)) == 0:
              ent = Entity(z1[0] + '_by_' + z2[0] + str(i))
              break

        ent.FK = [z1[1], z2[1]]
        ent.Parent[z1[0]] = 1
        ent.Parent[z2[0]] = 1
        Entities.append(ent)

        # добовляем связи с новой сущностью в изначальные
        for i, e in enumerate(Entities):
          if e.Name == z1[0]:
            if y[3] == '+': Entities[i].Child[ent.Name] = '1-M'
            if y[3] == '*': Entities[i].Child[ent.Name] = '0-M'
            e.OtherRelations.pop(z2[0])
            continue
          if e.Name == z2[0]:
            if y[0] == '+': Entities[i].Child[ent.Name] = '1-M'
            if y[0] == '*': Entities[i].Child[ent.Name] = '0-M'
            e.OtherRelations.pop(z1[0])
            continue

  dic = to_json_file(Entities, 2)
  with open("diagram2.json", "w") as write_file:
    json.dump(dic, write_file, indent=4)
  command = "python3 --version"

  os.system("erdot diagram2.json")
  os.system("dot diagram2.dot -Tpng -o diagram2.png")



