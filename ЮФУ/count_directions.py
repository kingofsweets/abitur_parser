
from operator import contains
from tika import parser # pip install tika
import pandas as pd
import re
import requests

#PEREFERENCES
CHUNK_SIZE = 2000
URL = 'https://sfedu.ru/00_main_2010/abitur/abit_2022/svodka/svodka_bak.pdf'
FILE_NAME = 'svodka_bak.pdf'

# GET RAW PDF FILE
def get_raw(url, filename, chunk_size):
        try:
                r = requests.get(url, stream=True)
                with open(filename, 'wb') as fd:
                        for chunk in r.iter_content(chunk_size):
                                fd.write(chunk)
                print("Файл успешно скачан...")
        except BaseException:
                print("Не удалось скачать файл...")

# PARSE RAW PDF FILE
def parse_raw_pdf(filename):
        print("Начало процесса извлечения текста...")
        raw = parser.from_file(filename)
        print(raw['content'])
        f = open('check.txt', 'w', encoding="utf-8")
        f.write(raw['content'])
        print("Текст успешно извлечён...")
        f.close()

def get_statistics_table(url, filename, chunk_size = 2000):
        get_raw(url, filename, chunk_size)
        parse_raw_pdf(filename)

        data = open('check.txt', 'r', encoding="utf-8").read()
        data = re.split(r'Суперсервис|Личный.прием|Доступно.в.webabit',data)[1:]

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

if __name__ == "__main__":
        get_statistics_table(URL, FILE_NAME, CHUNK_SIZE)