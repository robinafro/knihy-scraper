import requests
import json
import os

from bs4 import BeautifulSoup

urls = os.path.join(os.path.dirname(__file__), 'urls.json')

with open(urls) as json_file:
    urls = json.load(json_file)

search_url = "https://www.eknihyzdarma.cz/eshop-fulltext-search.html?q=" # later we will have multiple websites so this will be included in the JSON

def send_request_and_print_result(search_term):
    url = f"{search_url}{search_term}"
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        print("Response from the server:")
        
        # write response.text to a file
        with open('response.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error sending the request: {e}")

# Replace 'your_search_term_here' with the actual search term you want to use
send_request_and_print_result('your_search_term_here')