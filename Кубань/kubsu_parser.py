from bs4 import BeautifulSoup
import requests
import pandas as pd

links = ['http://ftp.kubsu.ru/alpha/02.03.03_792_ofo_b.html','http://ftp.kubsu.ru/alpha/09.03.03_793_ofo_b.html', 'http://ftp.kubsu.ru/alpha/09.04.02_1134_ofo_b.html', 'http://ftp.kubsu.ru/alpha/09.04.02_847_ofo_b.html' ]

def get_table(soup):
    name = [] # ФИО
    type = [] # ТИП ВИ

    table = soup.find('table')
    dir_log = table.find_all('div')
    print(dir_log[1].text)

    table = table.find('table')
    rows = table.find_all('tr')
    print(rows)
    for row in range(len(rows)):
        if row > 0:
            cols = rows[row].find_all('td')

            type.append(cols[2].text.split('\n')[1])
            name.append(cols[1].text.split('\n')[1])
    
    return {"ФИО": name,"Тип ВИ": type ,"Направление": dir_log[3].text}



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
    init_data.to_csv('KUBSU.csv')

main(links)
