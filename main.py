import requests
import os
import sys
import platform
import json

from bs4 import BeautifulSoup
from urllib.parse import quote
from unidecode import unidecode
import fitz  # PyMuPDF
from colorama import init, Fore

from wikipedia import get_book_info

config = json.load(open('config.json', 'r', encoding='utf-8'))
urls = json.load(open('urls.json', 'r', encoding='utf-8'))
books = json.load(open('books.json', 'r', encoding='utf-8'))
category_requirements = json.load(open('category_requirements.json', 'r', encoding='utf-8'))

all_args = []

for arg in sys.argv:
    all_args.append(arg.lower())

if config["download_dir"].startswith("/"):
    config["download_dir"] = config["download_dir"][1:]

if not config["download_dir"].startswith('\\'):
    config["download_dir"] = '\\' + config["download_dir"]

if not os.path.exists(os.path.expanduser('~') + config["download_dir"]):
    os.makedirs(os.path.expanduser('~') + config["download_dir"])

failed_books = []
corrupted_books = []

books_by_category = {}

def printfnc(text):
    if not "silent" in all_args:
        print(text)

def remove_special_characters(string):
    return "".join([c for c in string if c.isalpha() or c.isdigit() or c==' ']).rstrip()

def count_pdf_pages(pdf_path):
    try:
        with fitz.open(pdf_path) as pdf_document:
            return pdf_document.page_count
    except Exception as e:
        printfnc(f"Error counting pages: {e}")
        return None

def download_file(name=None, url=None, search_path=None, not_found_pattern=None, search_term=""):
    try:
        book_name = search_term.split(' - ')[1]

        printfnc(f"{Fore.LIGHTBLUE_EX}Searching for: {book_name}")
    
        book_name = quote(book_name.encode('windows-1250'), safe='')

        filename = os.path.join(os.path.expanduser('~') + config["download_dir"], remove_special_characters(search_term) + ".pdf")

        if not os.path.exists(filename):
            if "download" in all_args:
                search_url = f"{url}{search_path}{book_name} pdf"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                }

            
                response = requests.get(search_url, headers=headers)
                response.raise_for_status()

                found = True
                
                if response.text.find(not_found_pattern) != -1:
                    printfnc(f"{Fore.RED}Failed to find book - no search results")
                    return
                
                soup = BeautifulSoup(response.text, 'html.parser')

                download_link = soup.find('a', jsname="UWckNb")["href"]
                
                printfnc(f"{Fore.LIGHTBLUE_EX}Download link: {download_link}")
                
                file_response = requests.get(download_link)
                file_response.raise_for_status()
                
                with open(filename, 'wb') as file:
                    file.write(file_response.content)

                printfnc(f"{Fore.GREEN}File downloaded to: {filename}")
        else:
            printfnc(f"{Fore.YELLOW}File already exists")
        
        return filename

    except requests.exceptions.RequestException as e:
        printfnc(f"{Fore.RED}Error: {e}")

        failed_books.append(search_term)

def main():
    for url in urls:
        printfnc(f"{Fore.LIGHTBLUE_EX}Trying URL: " + url)

        data = urls[url]

        if data.get("disabled"):
            continue

        for category in books:
            for book_data in books[category]["books"]:
                book = book_data["name"]
                
                filename = download_file(name=url, url=data["url"], search_path=data["search_path"], not_found_pattern=data["not_found_pattern"], search_term=book)

                if filename is not None:
                    pages = count_pdf_pages(filename)
                    
                    if pages is not None:
                        if category not in books_by_category:
                            books_by_category[category] = {}

                        if book not in books_by_category[category]:
                            books_by_category[category][book] = {}

                        books_by_category[category][book]["page_count"] = pages
                    elif "download" in all_args:
                        corrupted_books.append(book)

                        if "deletecorrupted" in all_args:
                            printfnc(f"{Fore.RED}Deleting corrupted file: {filename}")
                            os.remove(filename)

                    if category not in books_by_category:
                        continue

                    if book not in books_by_category[category]:
                        continue

                    book_info = get_book_info(book)

                    book_info["release_date"] = book_info["release_date"] if book_info["release_date"] is not None else books[category]["default_release_date"]
                    book_info["author_nationality"] = book_info["author_nationality"] if book_info["author_nationality"] is not None else books[category]["default_author_nationality"]

                    print(Fore.LIGHTGREEN_EX + "  Release date: " + book_info["release_date"])
                    print(Fore.LIGHTGREEN_EX + "  Author nationality: " + book_info["author_nationality"])

                    books_by_category[category][book]["release_date"] = book_info["release_date"] or "unknown"
                    books_by_category[category][book]["author_nationality"] = book_info["author_nationality"] or "unknown"

if __name__ == "__main__":
    main()

    message = ""

    if "download" in all_args:
        message = f"{Fore.GREEN}Downloaded all available books." + (Fore.RED + " Failed to download: " if len(failed_books) > 0 else "")
    
    i = 0
    for book in failed_books:
        i += 1
        message += book + (", " if i < len(failed_books) else "")

    if len(corrupted_books) > 0:
        message += f"{Fore.RED} | Corrupted books: "

        i = 0
        for book in corrupted_books:
            i += 1
            message += book + (", " if i < len(corrupted_books) else "")

    printfnc(message)

    if len(failed_books) > 0:
        printfnc(Fore.MAGENTA + "FYI: If any books failed to download, it's probably caused by the website having policies against web scraping. If files are corrupted, the program will detect and optionally delete them. The reason for files being corrupted is unknown, most likely an issue on the server.")
    
    printfnc(Fore.CYAN + "Books by length:")

    for category, books_in_category in books_by_category.items():
        if "sort" in all_args:
            books_in_category = sorted(books_in_category.items(), key=lambda x: x[1].get("page_count", float('inf')))

        print(f"{Fore.LIGHTBLUE_EX}{category}:")
        for book, data in (books_in_category if "sort" in all_args else books_in_category.items()):
            page_count = data.get("page_count", float('inf'))

            if page_count is not None:
                print(f"{Fore.CYAN}{book}:   {page_count} pages")

    if "getminimum" in all_args:
        minimum_required_books = {}
        already_added_authors = []

        for category, books_in_category in books_by_category.items():
            for book, data in books_in_category.items():
                for name, requirements in category_requirements["categories"].items():
                    if requirements["satisfied"] < requirements["required"]:
                        if (int(data["release_date"]) >= int(requirements.get("minimum_release_date", data["release_date"]))) and (int(data["release_date"]) <= int(requirements.get("maximum", data["release_date"]))) and (data["author_nationality"] == requirements.get("author_nationality") or data["author_nationality"]):
                            if book in minimum_required_books:
                                continue

                            author = book.split(' - ')[0]

                            if author in already_added_authors:
                                continue

                            requirements["satisfied"] += 1
                            minimum_required_books[book] = data
                            already_added_authors.append(author)

        all_categories_merged = {}
        for category, books_in_category in books_by_category.items():
            for book, data in books_in_category.items():
                if all_categories_merged.get("category") is None:
                    all_categories_merged["category"] = {}
                
                all_categories_merged["category"][book] = data

        if len(minimum_required_books) < category_requirements["minimum_books"]:
            for category, books_in_category in all_categories_merged.items():
                for book, data in books_in_category.items():
                    if book in minimum_required_books:
                        continue

                    author = book.split(' - ')[0]

                    if author in already_added_authors:
                        continue

                    if len(minimum_required_books) >= category_requirements["minimum_books"]:
                        break

                    minimum_required_books[book] = data
                    already_added_authors.append(author)

                    print(f"{Fore.YELLOW}Added book {book} because there weren't enough books to satisfy the minimum requirements.")

        print("-" * 50)
        print(f"{Fore.CYAN}Minimum required books:")
        for book, data in minimum_required_books.items():
            print(f"{Fore.CYAN}  {book}: {data['page_count']} pages")


    print(Fore.WHITE)
