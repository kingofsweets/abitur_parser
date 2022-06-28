from bs4 import BeautifulSoup
import requests
import pandas as pd

links = ['https://kubsau.ru/upload/slpd/in_lists/main/52_09.03.02_000000743_%D0%94.html?0.30614371517791894','https://kubsau.ru/upload/slpd/in_lists/main/62_09.03.03_000000758_%D0%94.html?0.7913739163230615' ]

def get_table(soup):
    name = [] # ФИО

    table = soup.find('table')
    rows = table.find_all('tr')
    print(rows)
    for row in range(len(rows)):
        cols = rows[row].find_all('td')

        if row == 5:
            direction = cols[0].text

        if row > 8:
            name.append(cols[1].text)

    
    return {"ФИО": name, "Направление": direction}



def get_data(link):
    raw = requests.get(link, verify=False)
    print(raw.status_code)

    soup = BeautifulSoup(raw.content.decode('utf-8'), "html.parser")

    table = pd.DataFrame(get_table(soup))
    print(table)


    return table




def main(links):
    init_data = get_data(links[0])
    links = links[1:]

    for direct in links:
        res = get_data(direct)
        print(res)
        init_data = pd.concat([init_data, res], ignore_index = True)
    
    print(init_data)
    init_data.to_csv('KUBSAU.csv')

main(links)
