from ast import pattern
from operator import contains
from tika import parser # pip install tika
import pandas as pd
import re
import requests

url = 'https://sfedu.ru/00_main_2010/abitur/abit_2022/svodka/svodka_bak.pdf'
r = requests.get(url, stream=True)

with open('svodka_bak.pdf', 'wb') as fd:
    for chunk in r.iter_content(2000):
        fd.write(chunk)

pattern = []


raw = parser.from_file('svodka_bak.pdf')
print(raw['content'])
f = open('check.txt', 'w', encoding="utf-8")
f.write(raw['content'])
f.close()

data = open('check.txt', 'r', encoding="utf-8").read()
data = re.split(r'webabit.и.СуперСервис|СуперСервис.и.webabit|Личный.прием|webabit|СуперСервис',data)[1:]

directions = [["Направление"], ["Количество"]]

sum = 0

for i in data:
    raw = i.split('\n')
    str_list = list(filter(None, raw))
    print(str_list)
    direction = str_list[0] + " " + str_list[1]
    if direction not in directions[0]:
            directions[0].append(direction)
            directions[1].append(1)
            sum +=1
    else:
            index = directions[0].index(direction)
            directions[1][index] = directions[1][index] + 1
            sum +=1

df = pd.DataFrame({directions[0][0]: directions[0][1:], directions[1][0]: directions[1][1:]})

print(df.head(20))
print(df.sum())

df.to_csv("directions.csv")