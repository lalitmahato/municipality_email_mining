import requests
import time
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
import re

url = 'https://sthaniya.gov.np/gis/website/webdataquery.php?province=0'
page = requests.get(url, timeout=1000, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(page.content, 'html.parser')

tbl = soup.find('table')
table = pd.read_html(str(tbl))[0]

whole_data = []

table_data = np.array(table)

def extractEmail(url):
    mun_page = requests.get(url, timeout=1000, headers={'User-Agent': 'Mozilla/5.0'})
    page_soup = BeautifulSoup(mun_page.content, 'html.parser')
    page_content = page_soup.text
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', page_content)
    emails = ', '.join(emails)
    return emails


counter = 1
for td in table_data:
    print(counter)
    mun_url = 'http://'+td[5]
    print('Scrapping', 'http://'+td[5])
    email = extractEmail(mun_url)
    whole_data.append({
        'sn': td[0],
        'municipality': td[1],
        'District': td[2],
        'Local_level_Type': td[3],
        'Province': td[4],
        'website': mun_url,
        'Email': email,
    })
    counter = counter + 1
    print('Completed\n')
    break
try:
    pass
except ConnectionError