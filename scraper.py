from bs4 import BeautifulSoup
import requests
import pandas as pd

def main():
    """

    """

    wiki_url = 'https://en.wikipedia.org/wiki/Deserts_of_Australia'
    table_class = 'wikitable sortable'

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    }

    response = requests.get(wiki_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    deserts_table = soup.find('table', class_=table_class)
    rows = deserts_table.find_all('tr')
    table_data = []

    headers = []
    for th in rows[0].find_all('th'): #specify first row and go through each element
        header_text = th.get_text(strip=True) #find all <th> cells, strip removes whitespace
        headers.append(header_text)

    table_data = []
    for row in rows[1:]: #go through the remaining rows after the first
        cells = []
        for td in row.find_all('td'): #go through all table data cells in the row
            cell_text = td.get_text(strip=True) #append text of each cell to a cells list
            cells.append(cell_text) 
        table_data.append(cells) #append cells list to table_data

    df = pd.DataFrame(table_data, columns=headers)
    df.to_csv('deserts.csv', index=False)



if __name__ == "__main__":
    main()