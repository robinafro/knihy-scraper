import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import os

search_url = "https://www.eknihyzdarma.cz"

def download_file(base_url, search_path, search_term, download_directory):
    search_term_encoded = quote(search_term.encode('windows-1250'), safe='')

    url = f"{base_url}{search_path}{search_term_encoded}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        found = True

        if response.text.find("nepovedlo se vyhledat") != -1:
            found = False

        print(found)

        if found:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the download link using the specified class
            download_link = soup.find('a', class_='download-book-link format-pdf')['href']
            download_link = base_url + "/" + download_link

            print(f"Download link: {download_link}")

            # Download the file
            file_response = requests.get(download_link)
            file_response.raise_for_status()

            # Get the filename from the URL
            filename = os.path.join(download_directory, search_term + ".pdf")

            # Save the file to the local directory
            with open(filename, 'wb') as file:
                file.write(file_response.content)

            print(f"File downloaded to: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Replace 'Babička' with your actual search term
download_file(search_url, '/eshop-fulltext-search.html?q=', 'Babička', "C:\\Users\\actul\\Downloads\\DownloadedBooks")
