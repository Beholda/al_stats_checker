from bs4 import BeautifulSoup
import requests
import pandas as pd

"""
Due to the magic of cloudflare, this program using requests does not work.
Selenium is required.
"""

def main():
    """
    Access the list of ships by stats site, scrape data by ship class,
    organise into 
    """
    wiki_url = "https://azurlane.koumakan.jp/wiki/List_of_Ships_by_Stats"
    headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    }
    response = requests.get(wiki_url, headers=headers)
    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    soup = BeautifulSoup(response.content, "html.parser")

    destroyer_stats = get_shipclass_stats("Destroyers", soup)
    print(destroyer_stats)
    

def get_shipclass_stats(shipclass: str, soup) -> dict:
    
    table_class = "azltable sortable jquery-tablesorter" # each table organised into tabs is of this class
    class_heading = soup.find("h2", id_=shipclass)
    table_div = class_heading.parent.find_next_sibling() # get the tabber div after the header that contains the articles containing the tables
    stats_articles = table_div.find_all("article", class_="tabber_panel") # get each article which contain the tables


    ship_level_tables = {} # each ship class has four ship level tables at levels 1, 100, 120 and 125
    for article in stats_articles:
        ship_level_id = article.get('id')
        ship_level = ship_level_id.replace("tabber-", "")
        stats_table = article.find('table', class_=table_class)
        stats_rows = stats_table.find_all('tr')
        headers = []
        for th in stats_rows[0].find_all('th'):
            header_text = th.get_text(strip=True)
            headers.append(header_text)
        table_data = []
        for row in stats_rows[1:]:
            cells = []
            for td in row.find_all('td'):
                cell_text = td.get_text(strip=True)
                cells.append(cell_text)
            table_data.append(cells)
        table_df = pd.DataFrame(table_data, columns=headers)
        ship_level_tables[ship_level] = table_df
    return ship_level_tables
            
if __name__ == "__main__":
    main()