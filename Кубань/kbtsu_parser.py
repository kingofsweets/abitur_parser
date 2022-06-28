import requests
import pandas as pd

competitions = [14038, 14040, 14041, 14104]

competitions_decode = {"14038" : "09.03.01: Информатика и вычислительная техника", "14040" : "09.03.03: Прикладная информатика", "14041" : "09.03.04: Программная инженерия", "14104" : "10.03.01: Информационная безопасность"}
ex_type_decode = {3: "ЕГЭ", 2: "тест"}
source_decode = {0: "нет", 1: "да"}


def get_table(data):
    code = [] # Шифр ЛД
    name = [] # ФИО
    ex_type = [] # Тип ВИ
    source = [] # Наличие подлинника
    sum = [] # Количество баллов в сумме

    for person in data:
        code.append(person[0])
        name.append(person[1])
        ex_type.append(ex_type_decode[person[2]])
        source.append(source_decode[person[3]])
        sum.append(person[4])
    
    return {'Шифр ЛД': code, 'ФИО': name, 'Тип ВИ': ex_type, 'Наличие подлинника': source, 'Количество баллов в сумме': sum}



def get_data(link, code):
    raw = requests.get(link, verify=False)

    json = raw.json()['roll']

    direction = competitions_decode[str(code)]
    table = pd.DataFrame(get_table(json))

    table['Направление'] = direction

    return table


def main(competitions):
    init_data = get_data(f'https://ent.kubstu.ru/?rank=0&edlv=2&edfm=1&estp=1&hid=5&fid=516&id={competitions[0]}&psm=0', competitions[0])
    competitions = competitions[1:]

    for direct in competitions:
        res = get_data(f'https://ent.kubstu.ru/?rank=0&edlv=2&edfm=1&estp=1&hid=5&fid=516&id={direct}&psm=0', direct)
        print(res)
        init_data = pd.concat([init_data, res], ignore_index = True)
    
    print(init_data)
    init_data.to_csv('KBTSU.csv')

main(competitions)

