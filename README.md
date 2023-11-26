# knihy-scraper
web scraper na maturitní četbu

- stáhne všechny knihy jako .pdf
- porovná knihy podle velikosi abys nemusel číst (coming soon)
- seřadí knihy podle kategorií (coming soon)

# Instalace
- stáhni si repozitář `git clone https://github.com/actulurus/knihy-scraper.git`
- nainstaluj si python3 a pip (https://phoenixnap.com/kb/install-pip-windows)
- nainstaluj si knihovny `pip install -r requirements.txt`
- (optional:) v config.json nastav download_dir na složku, kam chceš stahovat knihy (pokud neexistuje, vytvoří se) (default je Downloads/DownloadedBooks)
- (optional:) pokud chceš stáhnout jen nějaké knihy, napiš je do books.json (formát musí zůstat stejný)
- spusť `python main.py` a užívej četbu