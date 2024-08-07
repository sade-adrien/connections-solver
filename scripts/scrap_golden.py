"""
This script scrapes the 400+ existing official connections games (from June 23 to August 24) from https://connections.swellgarfo.com/archive .
These will be our golden samples as they are directly taken from the official game.
""" 

from bs4 import BeautifulSoup
import requests
import json

base_url = 'https://connections.swellgarfo.com/nyt/'
output_file = 'data/connections_golden.json'

sample = []
for i in range(1,446):
    response = requests.get(base_url + str(i))
    soup = BeautifulSoup(response.text, 'html.parser')

    script = soup.find('script', {'id': '__NEXT_DATA__'})
    json_data = json.loads(script.string)

    data = json_data['props']['pageProps']['answers']

    output = {'idx': i, 'source': base_url, 'data': []}
    for item in data:
        output['data'].append(
            {
                'description': item['description'],
                'words': item['words'],
            }
        )

    sample.append(output)


with open(output_file, 'w') as file:
    json.dump(sample, file, indent=4)