import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

url="https://www.weinfuerst.de/products/lago-vero-garda-frizzante"

def extract_dynamic_wine_review(wine_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(wine_url)
        page.wait_for_selector("div#ReviewsWidget")
        content = page.content()
        soup = BeautifulSoup(content, 'html.parser')
        reviews_widget = soup.select("div.R-TextHeading.R-TextHeading--md.R-TextHeading--inline.u-marginBottom--none.u-marginRight--xs.u-verticalAlign--middle")[0].get_text(strip=True)
        browser.close()
        return reviews_widget


def extract_vivino_review(name):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the page
        page.goto("https://www.vivino.com/search/wines?q=" + name)

        # Wait for the page to fully load

        # Optionally, print the page content to inspect what is loaded
        content = page.content()

        # Extract the content and parse with BeautifulSoup
        soup = BeautifulSoup(page.content(), 'html.parser')

        # Try finding the reviews section
        reviews = soup.select("div.search-results-list")
        browser.close()

        print(reviews)  # Print the reviews or parsed data
        return reviews


# Example usage
#extract_vivino_review("Lago Vero Garda Frizzante")
