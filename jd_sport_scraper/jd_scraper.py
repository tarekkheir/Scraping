import requests
from bs4 import BeautifulSoup
import csv
import json
import textwrap
import re


url = "https://www.jdsports.fr"


def get_pages_links():
    req = requests.get(
        'https://www.jdsports.fr/homme/chaussures-homme/baskets/?max=100')
    print(req.status_code, url)
    soup = BeautifulSoup(req.text, 'html.parser')

    all_pages = soup.find("div", "pageLinks").find_all("a")
    pages_links = []

    for a in all_pages:
        link = a['href']
        pages_links.append(str(link))

    pages_links.pop(0)
    pages_links.pop()

    print(pages_links)
    return pages_links


def get_products_links(page_link):
    req = requests.get(page_link)
    print(req.status_code, page_link)
    soup = BeautifulSoup(req.text, 'html.parser')

    products = soup.find_all("li", class_="productListItem")
    products_links = []

    for p in products:
        products_links.append(p.find("a")['href'])

    print(products_links)
    return products_links


def get_products_data(url, products_links):

    products_data = []
    for link in products_links:
        req = requests.get(url + link)
        print(req.status_code, url + link)
        soup = BeautifulSoup(req.text, 'html.parser')

        js = soup.find_all('script')[3]
        data = js.string
        obj_brut = data.split('var dataObject = ')
        j2 = obj_brut[1].split(',')
        sub = '//'
        result = []

        for i in range(0, len(j2) - 1):
            dedent = textwrap.dedent(j2[i])
            s = re.split('\t|\n|{|}', dedent)
            for e in s:
                if e == '':
                    s.remove('')
                if sub in e:
                    s.remove(e)

            res = ('').join(s)
            result.append(res)
            if 'currency' in res:
                break

        datas = []
        for element in result:
            e = element.split(':')
            if e[0] == 'unitPrice':
                d = e[1].replace('"', '')
                datas.append(d)
            if e[0] == 'brand':
                d = e[1].replace('"', '')
                datas.append(d)
            if e[0] == 'description':
                d = e[1].replace('"', '')
                datas.append(d)
            if e[0] == 'sale':
                d = e[1].replace('"', '')
                datas.append(d)

        final_datas = (',').join(datas)
        print('datas: {}'.format(final_datas))
        products_data.append(final_datas)

    print(products_data)
    return products_data


def write_data_in_csv_file(pages_links):
    for i in range(0, len(pages_links)):
        product_links = get_products_links(url + pages_links[i])
        products_data = get_products_data(url, product_links)

        with open("jd_baskets_data.csv", 'a+', encoding="UTF-8", newline='') as f:
            writer = csv.writer(f, delimiter='\n')
            writer.writerow(products_data)


def sort_datas():
    marks = {
        "Nike": {"quantity": 0, "average_price": 0},
        "Vans": {"quantity": 0, "average_price": 0},
        "FredPerry": {"quantity": 0, "average_price": 0},
        "Jordan": {"quantity": 0, "average_price": 0},
        "EmporioArmaniEA7": {"quantity": 0, "average_price": 0},
        "UnderArmour": {"quantity": 0, "average_price": 0},
        "adidas": {"quantity": 0, "average_price": 0},
        "BOSS": {"quantity": 0, "average_price": 0},
        "Lacoste": {"quantity": 0, "average_price": 0},
        "Puma": {"quantity": 0, "average_price": 0},
        "NewBalance": {"quantity": 0, "average_price": 0},
        "Fila": {"quantity": 0, "average_price": 0},
        "Converse": {"quantity": 0, "average_price": 0},
        "Asics": {"quantity": 0, "average_price": 0},
        "Salomon": {"quantity": 0, "average_price": 0},
        "Onrunning": {"quantity": 0, "average_price": 0},
        "Napapijri": {"quantity": 0, "average_price": 0},
        "McKenzie": {"quantity": 0, "average_price": 0},
        "Birkenstock": {"quantity": 0, "average_price": 0},
        "Reebok": {"quantity": 0, "average_price": 0},
    }

    with open("jd_baskets_data.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            s = line.split(',')
            if len(s) > 1:
                m = s[3].split('\n')
                split_mark = m[0].replace(' ', '')
                for key in marks.keys():
                    if key in split_mark:
                        marks[key]["quantity"] += 1
                        marks[key]["average_price"] += float(
                            s[1].replace(' ', ''))
        f.close()

    for mark in marks:
        q = marks[mark]["quantity"]
        if q > 0:
            marks[mark]["average_price"] = round(
                (marks[mark]["average_price"] / q), 2)

    with open("data.json", "w+") as f:
        json.dump(marks, f)
        f.close()


pages_links = get_pages_links()
write_data_in_csv_file(pages_links)
sort_datas()
