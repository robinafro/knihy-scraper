import wikipediaapi
import sys

def get_book_info(book_query):
    user_agent = "knihy-scraper/1.0 (actulurus@gmail.com)"
    wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language='cs')

    author_name, book_name = map(str.strip, book_query.split(' - ', 1))

    release_date = None
    page = wiki_wiki.page(book_name)
    if page.exists():
        for word in page.summary.split(' '):
            if word.find('.') != -1:
                word = word[:word.find('.')]
            
            word = ''.join(filter(str.isalnum, word))

            if word.isdigit() and len(word) == 4:
                release_date = word
                break

    author_nationality = None
    author_page = wiki_wiki.page(author_name)
    
    if author_page.exists():
        author_nationality = "czech" if "český" in author_page.summary.lower() else "not_czech"

    return {
        'book_name': book_name,
        'author_name': author_name,
        'release_date': release_date,
        'author_nationality': author_nationality
    }
