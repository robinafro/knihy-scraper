import requests
import os
import json

from bs4 import BeautifulSoup
from urllib.parse import quote
from unidecode import unidecode

# Specify the encoding when reading the JSON files
config = json.load(open('config.json', 'r', encoding='utf-8'))
urls = json.load(open('urls.json', 'r', encoding='utf-8'))
books = json.load(open('books.json', 'r', encoding='utf-8'))

def remove_special_characters(input_string):
    # Convert to lowercase and transliterate Unicode characters to ASCII
    normalized_string = unidecode(input_string.lower())
    
    # Remove non-alphanumeric characters
    normalized_string = ''.join(char for char in normalized_string if char.isalnum() or char.isspace())
    
    return normalized_string

def download_file(name=None, url=None, search_path=None, download_class=None, not_found_pattern=None, search_term=""):
    book_name = search_term.split(' - ')[1]

    print(f"Searching for: {book_name}")

    book_name = quote(book_name.encode('windows-1250'), safe='')

    filename = os.path.join(config["download_dir"], search_term + ".pdf")

    if os.path.exists(filename):
        print("File already exists")
        return

    search_url = f"{url}{search_path}{book_name}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        found = True
        
        if response.text.find(not_found_pattern) != -1:
            found = False

        if found:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the download link using the specified class
            download_link = soup.find('a', class_=download_class)
            
            if not download_link:
                print("Failed to find book - no download link found")
                return
            
            download_link = download_link.get('href')

            download_link = url + "/" + download_link

            print(f"Download link: {download_link}")

            # Download the file
            file_response = requests.get(download_link)
            file_response.raise_for_status()
            
            # Save the file to the local directory
            with open(filename, 'wb') as file:
                file.write(file_response.content)

            print(f"File downloaded to: {filename}")
        else:
            print("Failed to find book - no search results")
            return

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def main():
    for url in urls:
        print("Trying URL: " + url)

        data = urls[url]

        for category in books:
            for book in books[category]:
                download_file(name=url, url=data["url"], search_path=data["search_path"], download_class=data["download_class"], not_found_pattern=data["not_found_pattern"], search_term=book)
            
if __name__ == "__main__":
    main()
