import requests
from bs4 import BeautifulSoup

def cryptocurrency_rate_parser(name: str):

    try:
        # Send a GET request to the CoinMarketCap page for the given cryptocurrency
        page = requests.get(f"https://coinmarketcap.com/currencies/{name}/")
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(page.text, 'lxml')

        # Find the HTML tag that contains the cryptocurrency price
        price_tag = soup.find('span', class_='sc-65e7f566-0 clvjgF base-text')

        return float(price_tag.text.replace(',', '').replace('$', ''))

    except:
        return None


if __name__ == '__main__':
    print(cryptocurrency_rate_parser("notcoin"))