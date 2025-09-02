from bs4 import BeautifulSoup
import requests
import pandas as pd

wiki_url = "https://en.wikipedia.org/wiki/List_of_current_United_States_representatives"
table_id = 'votingmembers'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
           "AppleWebKit/537.36 (KHTML, like Gecko)"
           "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}

response = requests.get(wiki_url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', attrs={'id': table_id})
rows = table.find_all('tr')
table_data = []

headers = []
for th in rows[0].find_all('th'):
    header_text = th.get_text(strip=True)
    headers.append(header_text)

table_data = []
for row in rows[1:]:
    cells = []
    for th in row.find_all('td'):
        cell_text = th.get_text(strip=True)
        cells.append(cell_text)
    table_data.append(cells)

df = pd.DataFrame(table_data, columns=headers)
df.to_csv('representatives.csv', index=False)
print(df.head())