from bs4 import BeautifulSoup
import requests
import pandas as pd

source = 'https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition='

competitions = [1712417222681472310, 1712416831985200438, 1712417235799158070, 1712417616938708278, 1712417608956947766, 1714956156281072950, 1712417600979381558, 1712417591424757046, 1712417582796025142, 1712417388938439990]

def get_table(soup):
    num = [] # Номер
    snils = [] # СНИЛС
    accept = [] # Согласие на зачисление
    source = [] # Наличие подлинника
    place = [] # Потребность в общежитии
    marks = [] # Оценки
    sum = [] # Сумма баллов за ВИ
    add = [] # Балл за ИД
    full = [] # Сумма баллов
    secondary = [] # Примечание

    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')

        num.append(cols[0].text)
        snils.append(cols[1].text)
        accept.append(cols[2].text)
        source.append(cols[3].text)
        place.append(cols[4].text)
        marks.append(cols[5].text)
        sum.append(cols[6].text)
        add.append(cols[7].text)
        full.append(cols[8].text)
        secondary.append(cols[9].text)
    
    return {num[0]: num[1:], snils[0]: snils[1:], accept[0]: accept[1:], source[0]: source[1:], place[0]: place[1:], sum[0]: sum[1:], add[0]: add[1:],  full[0]: full[1:],  secondary[0]: secondary[1:], marks[0]: marks[1:] }



def get_data(link):
    raw = requests.get(link)
    print(raw.status_code)

    soup = BeautifulSoup(raw.text, "html.parser")

    direction = soup.find('h1').text
    table = pd.DataFrame(get_table(soup))

    table['Направление'] = direction.split('\t')[2]

    return table




def main(source, competitions):
    init_data = get_data(source + str(competitions[0]))
    competitions = competitions[1:]

    for direct in competitions:
        res = get_data(source + str(direct))
        print(res)
        init_data = pd.concat([init_data, res], ignore_index = True)
    
    print(init_data)
    init_data.to_csv('MIREA.csv')

main(source, competitions)


