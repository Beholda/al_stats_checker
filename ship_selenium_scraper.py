from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

def main():
    website = "https://azurlane.koumakan.jp/wiki/List_of_Ships_by_Stats"
    service = Service(executable_path='C:/Users/simad/OneDrive/Documents/edgedriver_win64/msedgedriver.exe')
    driver = webdriver.Edge(service=service)
    driver.get(website)
    
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.ID, "Destroyers")))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    ship_classes = ["Destroyers", "Light_Cruisers", "Heavy_Cruisers_and_Large_Cruisers", 
                    "Battleships,_Battlecruisers,_Aviation_Battleships_and_Monitors",
                    "Aircraft_Carriers_and_Light_Aircraft_Carriers",
                    "Submarines_and_Submarine_Carriers", "Auxiliaries",
                    "Sailing_Frigates_(Submarine),_Sailing_Frigates_(Vanguard)_and_Sailing_Frigates_(Main)"]
    
    ship_class_map = {
        "Destroyers": "DD",
        "Light_Cruisers": "CL",
        "Heavy_Cruisers_and_Large_Cruisers": "CA",
        "Battleships,_Battlecruisers,_Aviation_Battleships_and_Monitors": "BB",
        "Aircraft_Carriers_and_Light_Aircraft_Carriers": "CV",
        "Submarines_and_Submarine_Carriers": "SS",
        "Auxiliaries": "AUX",
        "Sailing_Frigates_(Submarine),_Sailing_Frigates_(Vanguard)_and_Sailing_Frigates_(Main)": "IX"
    }
    
    # search the soup for each ship class and use the function to extract the table data
    # each ship_level_table is a dict the key being the level e.g. Level_100 and value being a pandas dataframe
    for ship_class in ship_classes: 
        shorthand = ship_class_map[ship_class]
        ship_level_tables = get_shipclass_stats(ship_class, soup)
        for level, df in ship_level_tables.items():
            folder_path = os.path.join(os.path.dirname(__file__), "ship_stats_data")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            csv_filename = f"{shorthand}_{level}.csv"
            df.to_csv(os.path.join(folder_path, csv_filename), index=False)
            
def get_shipclass_stats(shipclass: str, soup) -> dict:
    
    class_heading = soup.find("h2", id=shipclass)
    table_div = class_heading.parent.find_next_sibling() # get the tabber div after the header that contains the articles containing the tables
    stats_articles = table_div.find_all("article", class_="tabber__panel") # get each article which contain the tables


    ship_level_tables = {} # each ship class has four ship level tables at levels 1, 100, 120 and 125

    # loop through each article, with each containing a table of the levels 1, 100, 120 and 125
    for article in stats_articles:
        ship_level_id = article.get('id') # extract the ID of the ship level, i.e. 1, 120, etc.

        # take the raw extracted ID e.g. tabber-Level_100_4
        # use a regular expression to recognise the ship level to turn it into Level_100
        match = re.search(r"(Level_\d+)", ship_level_id) 
        if match:
            ship_level = match.group(1)

        stats_table = article.find('table', class_="azltable")
        stats_rows = stats_table.find_all('tr')
        headers = []
        for th in stats_rows[0].find_all('th'):

            header_text = th.get_text(strip=True)
            if not header_text:
                span = th.find("span", title=True)
                if span:
                    header_text = span['title']
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
