from bs4 import BeautifulSoup
import requests
import pandas as pd

def main():
    """
    Access the list of ships by stats site, scrape data by ship class,
    organise into 
    """
    wiki_url = "https://azurlane.koumakan.jp/wiki/List_of_Ships_by_Stats"
    table_class = "azltable sortable jquery-tablesorter" # each table organised into tabs is of this class

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    }

    response = requests.get(wiki_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    stats_table = soup.find('table', class_ = table_class)
    rows = stats_table.find_all('tr')
    

if __name__ == "__main__":
    main()