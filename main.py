import requests
import os
import platform
import json

from bs4 import BeautifulSoup
from urllib.parse import quote
from unidecode import unidecode

# Specify the encoding when reading the JSON files
config = json.load(open('config.json', 'r', encoding='utf-8'))
urls = json.load(open('urls.json', 'r', encoding='utf-8'))
books = json.load(open('books.json', 'r', encoding='utf-8'))

if platform.system() == "Linux" and config["download_dir"].startswith("C:"):
    print("You're on Linux but the download directory starts with C: - please change it in config.json")
    exit()

if not os.path.exists(config["download_dir"]):
    os.makedirs(config["download_dir"])

def remove_special_characters(string):
    return "".join([c for c in string if c.isalpha() or c.isdigit() or c==' ']).rstrip()

def download_file(name=None, url=None, search_path=None, not_found_pattern=None, search_term=""):
    book_name = search_term.split(' - ')[1]

    print(f"Searching for: {book_name}")

    book_name = quote(book_name.encode('windows-1250'), safe='')

    filename = os.path.join(config["download_dir"], remove_special_characters(search_term) + ".pdf")

    if os.path.exists(filename):
        print("File already exists")
        return

    search_url = f"{url}{search_path}{book_name} pdf"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        found = True
        
        if response.text.find(not_found_pattern) != -1:
            print("Failed to find book - no search results")
            return
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        download_link = soup.find('a', jsname="UWckNb")["href"]
        
        print(f"Download link: {download_link}")

        # Download the file
        file_response = requests.get(download_link)
        file_response.raise_for_status()
        
        # Save the file to the local directory
        with open(filename, 'wb') as file:
            file.write(file_response.content)

        print(f"File downloaded to: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def main():
    for url in urls:
        print("Trying URL: " + url)

        data = urls[url]

        if data.get("disabled"):
            continue

        for category in books:
            for book in books[category]:
                download_file(name=url, url=data["url"], search_path=data["search_path"], not_found_pattern=data["not_found_pattern"], search_term=book)
            
if __name__ == "__main__":
    main()
