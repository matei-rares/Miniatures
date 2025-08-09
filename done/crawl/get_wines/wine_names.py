import requests
from bs4 import BeautifulSoup
import csv
import time
from dynamic_load import extract_dynamic_wine_review
import time
import pandas as pd

DEFAULT_URL = 'https://vinregal.ro'  # + '/collections/all/products/lagona-rose-2019'
BASE_COLLECTION_URL = 'https://vinregal.ro/collections/all'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


class Wine:
    def __init__(self, name: str, price: float, type: str, grape: str, country: str, litres: str, alc_per: float,
                 vivino_rev: float, wunder_rev: float):
        self.name = name
        self.price = price
        self.type = type
        self.grape = grape
        self.country = country
        self.litres = litres
        self.alc_per = alc_per
        self.vivino_rev = vivino_rev
        self.wunder_rev = wunder_rev

    def __repr__(self):
        return (f"Wine(name={self.name}, price={self.price}, alc_per={self.alc_per}, "
                f"vivino_rev={self.vivino_rev}, wunder_review={self.wunder_rev})")


# Sort wines by vivino_rev (desc), wunder_review (desc), and price (asc)

def save_to_excel(wines, filename="wines.xlsx"):
    data = [{"Name": wine.name, "Price": wine.price, "Type": wine.type, "Grape": wine.grape,
             "Country": wine.country, "Litres": wine.litres, "Alc_Per": wine.alc_per,
             "Vivino_Rev": wine.vivino_rev, "Wunder_Review": wine.wunder_rev} for wine in wines]
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)


def extract_wine_from_page(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    divs = soup.select('div.product-item')
    wines = []
    for div in divs:
        if div.select_one('img'):
            # imgs.append(div.select_one('img'))
            name = div.select_one('img').get('alt')
            print(name)
            price = float(
                div.select_one('span.price').get_text(strip=True).replace(" lei", '').replace(",", '.'))  # price
            print(price)
            link = div.select_one('a').get('href')
            wines.append(extract_properties(link, name, price))

    print(wines)

    return wines

    # prod= soup.select('div.product-item img')
    # prod_names = [a.get('alt') for a in prod ]


def extract_properties(link, name, price):
    try:
        soup = BeautifulSoup(requests.get(DEFAULT_URL + link, headers=HEADERS).content, 'html.parser')

        list = soup.select("div.product-block-list__item--profile")[1].select_one('ul').select("li")
        text = []
        for prop in list:
            text.append(prop.get_text(strip=True))
        print(text)
        w_type = text[1].replace("Tip vin", '')
        grape = text[2].replace("Soi struguri", '')
        country = text[3].replace("Țară", '')
        if 'Regiune' not in text[4]:
            litres = text[4].replace("Cantitate", '').replace("\n              L", '')
            alc_per = float(text[5].replace("Conținut alcool", '').replace(" % vol", '').replace(",", "."))
        else:
            litres = text[5].replace("Cantitate", '').replace("\n              L", '')
            alc_per = float(text[6].replace("Conținut alcool", '').replace(" % vol", '').replace(",", "."))
        print(w_type, grape, country, litres, alc_per)

        # take from vivino
        soup = BeautifulSoup(requests.get("https://www.vivino.com/search/wines?q=" + name, headers=HEADERS).content,
                             'html.parser')
        if len(soup.select("div.search-results-list")) >= 1:
            vivino_rev = float(soup.select("div.search-results-list")[0].select_one(
                "div.text-inline-block.light.average__number").get_text(strip=True).replace(",", ".").replace('—', "0"))
        else:
            vivino_rev = 0
        print(vivino_rev)  # average rating vivino

        # take from weinfuerst
        wunder_rev = float(extract_dynamic_wine_review(
            "https://www.weinfuerst.de/products/" + link.split("/")[-1]))  # average rating weinfuerst
        print(wunder_rev)
    except Exception as e:
        print(e)
        return Wine(name, price, "N/A", "N/A", "N/A", "N/A", 0, 0, 0)
    return Wine(name, price, w_type, grape, country, litres, alc_per, vivino_rev, wunder_rev)


def main():
    # extract_wine_details(BASE_URL)

    page_number = 2
    all_wines=[]
    all_wines = extract_wine_from_page(BASE_COLLECTION_URL)

    while page_number < 8:
        page_url = f'{BASE_COLLECTION_URL}/?page={page_number}'
        wines = extract_wine_from_page(page_url)
        all_wines.extend(wines)
        page_number += 1
    sorted_wines = sorted(all_wines, key=lambda w: (-w.vivino_rev, -w.wunder_rev, w.price))
    print(sorted_wines)
    save_to_excel(sorted_wines)

if __name__ == '__main__':
    main()
