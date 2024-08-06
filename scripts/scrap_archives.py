"""
This script scrapes the 400+ existing official connections games (from June 23 to August 24) from https://connections.swellgarfo.com/archive .
""" 

from bs4 import BeautifulSoup
import requests
import json

base_url = 'https://connections.swellgarfo.com/nyt/'
output_file = 'data/connections_archives.json'

sample = []
for i in range(1, 10):#446
    response = requests.get(base_url + str(i))
    soup = BeautifulSoup(response.text, 'html.parser')

    script = soup.find('script', {'id': '__NEXT_DATA__'})
    json_data = json.loads(script.string)

    data = json_data['props']['pageProps']['answers']

    output = []
    for item in data:
        output.append({
            'description': item['description'],
            'words': item['words']
        })

    sample.append([{'idx': i}, output])


with open(output_file, 'w') as file:
    json.dump(sample, file, indent=4)