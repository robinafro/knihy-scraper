import requests
from bs4 import BeautifulSoup

def scrape_crypto_news(urls):
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract relevant information from the webpage
        # Modify this part based on the structure of the website
        articles = soup.find_all('h2')

        for article in articles:
            # Check if the article is related to Bitcoin
            if 'bitcoin' in article.text.lower():
                print(f"Website: {url}")
                print(f"Title: {article.text}")
                print("\n" + "=" * 50 + "\n")  # Separating articles for clarity

# Example URLs for crypto news
crypto_news_urls = ['https://coindesk.com/', 'https://coinmarketcap.com/']
scrape_crypto_news(crypto_news_urls)
