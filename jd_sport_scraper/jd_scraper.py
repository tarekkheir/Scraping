import requests
from bs4 import BeautifulSoup
import csv
import json


url = "https://www.jdsports.fr"

def get_pages_links():
    req = requests.get('https://www.jdsports.fr/homme/chaussures-homme/baskets/?max=100')
    print(req.status_code, url)
    soup = BeautifulSoup(req.text, 'html.parser')

    all_pages = soup.find("div", "pageLinks").find_all("a")
    pages_links = []

    for a in all_pages:
        link = a['href']
        pages_links.append(str(link))

    pages_links.pop(0)
    pages_links.pop()

    return pages_links

def get_products_links(page_link):
    req = requests.get(page_link)
    print(req.status_code, page_link)
    soup = BeautifulSoup(req.text, 'html.parser')
    
    products = soup.find_all("li", class_="productListItem")
    products_links = []

    for p in products:
        products_links.append(p.find("a")['href'])

    return products_links


def get_products_data(url, products_links):

    products_data = []
    for link in products_links:
        req = requests.get(url + link)
        print(req.status_code, url + link)
        s = BeautifulSoup(req.text, 'html.parser')

        name = s.find(id="productItemTitle").find("h1").text
        price = s.find("span", class_="pri").text
        data = name + ": " + price
        print(data)
        products_data.append(data)

        print(data)
    
    return products_data


def write_data_in_csv_file(pages_links):
    for i in range(0, len(pages_links)):
        product_links = get_products_links(url + pages_links[i])
        print("\nPAGE {} content\n".format(i+1))
        products_data = get_products_data(url , product_links)

        with open("jd_baskets_data.csv", 'a+', encoding="UTF-8", newline='') as f:
            p = "\nPAGE {}\n".format(i+1)
            f.write(p)
            writer = csv.writer(f, delimiter='\n')
            writer.writerow(products_data)



def sort_datas():
    marks = {
        "Nike": {"quantity": 0, "average_price": 0},
        "Tommy": {"quantity": 0, "average_price": 0},
        "Vans": {"quantity": 0, "average_price": 0},
        "Fred": {"quantity": 0, "average_price": 0},
        "Jordan": {"quantity": 0, "average_price": 0},
        "Emporio": {"quantity": 0, "average_price": 0},
        "Under": {"quantity": 0, "average_price": 0},
        "adidas": {"quantity": 0, "average_price": 0},
        "BOSS": {"quantity": 0, "average_price": 0},
        "Lacoste": {"quantity": 0, "average_price": 0},
        "Puma": {"quantity": 0, "average_price": 0},
        "New": {"quantity": 0, "average_price": 0},
        "Fila": {"quantity": 0, "average_price": 0},
        "Converse": {"quantity": 0, "average_price": 0},
        "Asics": {"quantity": 0, "average_price": 0},
        "Salomon": {"quantity": 0, "average_price": 0},
        "On": {"quantity": 0, "average_price": 0}   
    }

    with open("jd_baskets_data.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            l = line.split(': ')
            if len(l) > 1:
                mark = l[0].split(' ')[0]
                price = int(l[1].split(',')[0])
                marks[mark]["quantity"] += 1
                marks[mark]["average_price"] += price
        f.close()

    for mark in marks:
        q = marks[mark]["quantity"]
        if q > 0:
            marks[mark]["average_price"] = round((marks[mark]["average_price"] / q), 2)

    
    with open("data.json", "w+") as f:
        json.dump(marks, f)
        f.close()

pages_links = get_pages_links()
write_data_in_csv_file(pages_links)
sort_datas()
