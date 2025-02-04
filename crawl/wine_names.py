import requests
from bs4 import BeautifulSoup
import csv
import time
from dynamic_load import extract_dynamic_wine_review

BASIC_URL = 'https://vinregal.ro' # + '/collections/all/products/lagona-rose-2019'
BASE_URL = 'https://vinregal.ro/collections/all'

# Headers to mimic a browser request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

class Wine:
    def __init__(self, name, price, year, country, url):
        self.name = name
        self.price = price
        self.year = year
        self.country = country
        self.url = url

    def __repr__(self):
        return f'<Wine {self.name}>'

    def to_dict(self):
        return {
            'Name': self.name,
            'Price': self.price,
            'Year': self.year,
            'Country': self.country,
            'URL': self.url
        }

def get_wine_links(page_url):
    response = requests.get(page_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Adjust the selector based on the website's structure
    wine_links = [a['href'] for a in soup.select('a.product-link') if 'href' in a.attrs]

    return wine_links




def extract_wine_from_page():
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    #select alt attribute from all images that are inside a div with class product-item

    divs=soup.select('div.product-item')
    #print(divs[0])
    imgs=[]

    for div in divs:
        if div.select_one('img'):
            imgs.append(div.select_one('img'))
            name=div.select_one('img').get('alt')
            print(name)
            print(div.select_one('span.price').get_text(strip=True))

            link=div.select_one('a').get('href')
            extract_properties(link)

            break
    # prod= soup.select('div.product-item img')
    # prod_names = [a.get('alt') for a in prod ]



def extract_properties(link):
    print(link.split("/")[-1])
    url=BASIC_URL+link
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    list=soup.select("div.product-block-list__item--profile")[1].select_one('ul').select("li")
    text=[]
    for prop in list:
        text.append(prop.get_text(strip=True))

    print(text[1].replace("Tip vin",''))
    print(text[3].replace("Țară", ''))
    print(text[5].replace("Cantitate", '').replace("\n              ", ''))
    print(text[6].replace("Conținut alcool", '').replace("vol", ''))
    print(text)


    response = requests.get("https://www.vivino.com/search/wines?q=" + "Lago Vero Garda Frizzante", headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.select("div.search-results-list")[0].select_one("div.text-inline-block.light.average__number").get_text(strip=True)) #average rating vivino


    url = "https://www.weinfuerst.de/products/" + link.split("/")[-1]
    print(url)
    print(extract_dynamic_wine_review(url)) # average rating weinfuerst





def main():
    extract_wine_from_page()
    #extract_wine_details(BASE_URL)


    pass
    page_number = 1
    all_wines = []

    while True: #TODO loop through all 7 pages
        page_url = f'{BASE_URL}/?page={page_number}'
        wine_links = get_wine_links(page_url)

        if not wine_links:
            break  # Exit loop if no more products

        for link in wine_links:
            time.sleep(1)  # Be polite to the server

        page_number += 1

    # Save data to CSV
    with open('vinregal_wines.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Name', 'Price', 'Description', 'URL'])
        writer.writeheader()
        writer.writerows(all_wines)

    print(f'Successfully scraped {len(all_wines)} wines.')


if __name__ == '__main__':
    main()




