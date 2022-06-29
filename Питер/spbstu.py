import requests
import pandas as pd

competitions = [184, 14040, 14041, 14104]

competitions_decode = {"184" : "02.03.03 Математическое обеспечение и администрирование информационных систем", 
                       "14040" : "09.03.03: Прикладная информатика", 
                       "14041" : "09.03.04: Программная инженерия", 
                       "14104" : "10.03.01: Информационная безопасность"}
original_decode = {True: "да", False: "нет"}
lgota_decode = {True: "нет", False: "да"}


def get_table(data):
    lgota = [] # Наличие льгот
    original = [] # Оригинал
    snils = [] # Снилс
    sum = [] # Сумма баллов
    ege = []

    for person in data:
        lgota.append(lgota_decode[person['no_have_lgota']])
        original.append(original_decode[person['has_original']])
        snils.append(person['users']['snils'])
        ege_p = person['ege']['result_ege']

        if len(ege_p) == 3:
            ege.append(f"{ege_p[0]['name']}/{ege_p[1]['name']}/{ege_p[2]['name']}")
            sum.append(ege_p[0]['result'] +ege_p[1]['result'] + ege_p[2]['result'])
        else:
            ege.append("Нет")
            sum.append(0)
        

    return {'СНИЛС': snils, 'Оригинал': original, 'Льготы': lgota, 'ЕГЭ': ege,  'Сумма': sum }



def get_data(link):
    raw = requests.get(link, verify=False)

    json = raw.json()['data']

    direction = competitions_decode[str(code)]
    table = pd.DataFrame(get_table(json))

    table['Направление'] = direction
    print(table)

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

