import requests
from bs4 import BeautifulSoup
import json
import re
import locale
locale.getlocale()
locale.setlocale(locale.LC_TIME, 'hu_HU') 
import datetime

url = "https://www.mnb.hu/arfolyamok"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find the table containing the data
table = soup.find_all("table")
day_string = soup.find("caption", {"class": "ttl ttl-s"}).get_text()
pattern = r'\d{4}\. \w+ \d+\.'

matches = re.search(pattern, day_string)
if matches:
    date_part = matches.group()
    date_part = datetime.datetime.strptime(date_part, '%Y. %B %d.')
    date_part = date_part.strftime('%Y-%m-%d')
else:
    print("Date not found.")


# Extract table rows
def get_data(id, date_part):
    exchange_rates = []
    rows = table[id].find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if cells:
            row_data = [cell.text.strip() for cell in cells]
            exchange_rates.append(
                {
                    "deviza_id":row_data[0],
                    "description":row_data[1],
                    "rate":row_data[3],
                    "date": date_part
                }
            )
    return exchange_rates
            



first_table = get_data(0, date_part)
second_table = get_data(1, date_part)
full_table = first_table + second_table

# Save the list of products as JSON
with open("data/exchange_rates.json", "w", encoding="UTF-8") as json_file:
    json.dump(full_table, json_file, indent=4, ensure_ascii=False)

        
