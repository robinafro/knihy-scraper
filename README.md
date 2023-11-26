# knihy-scraper
web scraper na maturitní četbu

- stáhne všechny knihy jako .pdf
- seřadí knihy podle velikosi
- vybere vám nejkratší knihy z každé kategorie.

# Instalace
- stáhni si repozitář `git clone https://github.com/actulurus/knihy-scraper.git`
- nainstaluj si python3 a pip (https://phoenixnap.com/kb/install-pip-windows)
- nainstaluj si knihovny `pip install -r requirements.txt`
- (optional:) v `config.json` nastav download_dir na složku, kam chceš stahovat knihy (pokud neexistuje, vytvoří se) (default je `Downloads/DownloadedBooks`)
- (optional:) pokud chceš stáhnout jen nějaké knihy, napiš je do `books.json` (formát musí zůstat stejný)

# Použití
- spusť `python main.py` s parametrem `download` pro stažení knih
- pokud chceš knihy seřadit podle délky, spusť `python main.py` s parametrami `sort`
- pokud z nějakého důvodu nechceš debug logy, spusť `python main.py` s parametrem `silent`
- pokud chceš automaticky smazat koruptované .pdf soubory, spusť `python main.py` s parametrem `deletecorrupted`

# Disclaimer
- občas se stane, že se nějakou knihu nepodaří stáhnout. ve většině případů je to způsobeno anti-botovskou ochranou, kterou má server, ze kterého se kniha stahuje. pokud opravdu moc chcete číst, je v takovém případě je potřeba knihu stáhnout ručně.
- občas se také některá kniha stáhne, ale je poškozena. to fakt neni muj problém, pravděpodobně maj dosraný servery - můžete použít parametr `deletecorrupted`, který smaže všechny poškozené knihy.

- jo a kdyžtak se tohle dá použít na jiný věci než knihy, ale musí to být PDF soubory.

# Licence
- dějej si s tim co chceš, ale nepudu za tebe do vězení za web scraping