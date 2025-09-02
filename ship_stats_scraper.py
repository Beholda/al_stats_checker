from bs4 import BeautifulSoup
import requests
import pandas as pd

wiki_url = "https://azurlane.koumakan.jp/wiki/List_of_Ships_by_Stats"
table_class = "azltable sortable jquery-tablesorter"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
           "AppleWebKit/537.36 (KHTML, like Gecko)"
           "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}

response = requests.get(wiki_url, headers=headers)
