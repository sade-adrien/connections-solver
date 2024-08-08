"""
This script scrapes samples from https://www.connectionsunlimited.org/ which provides more human-made examples but unnoficial.
They are not from the original game and we're unsure about the method of creation or their quality in regards to the original game. We qualify those examples as silver.
We manually extracted the js database into data/raw_silver.js. This script extract the examples from the raw file.
"""

import json
import re


input_path = 'data/raw_silver.js'
output_path = 'data/connections_silver.json'
golden_path = 'data/connections_golden.json'

with open(input_path, 'r') as file:
    data = file.read()

# Clean to allow json.loads
extracted_data = re.search(r"JSON\.parse\('(.*?)'\)", data).group(1)
extracted_data = re.sub(r'\\u[0-9a-fA-F]{4}', '', extracted_data)      #remove unicodes
extracted_data = re.sub(r"""\\\\"|\\"|\\'""", "'", extracted_data)     #remove superfluous \\quotes

json_data = json.loads(extracted_data)


# Read existing golden samples to avoid duplication
with open(golden_path, 'r') as file:
    golden_json = json.load(file)

golden_samples = []
for gs in golden_json:
    words_set = {word for item in gs['data'] for word in item['words']}
    golden_samples.append(words_set)


samples = []
idx = 1
for item in json_data:
    output = {'idx': idx, 'source': 'https://www.connectionsunlimited.org/', 'data': []}
    for group, details in item['groups'].items():
        output['data'].append(
            {
                'description': group,
                'words': details['members'],
            }
        )
    
    words_set = {word for item in output['data'] for word in item['words']}
    if words_set in golden_samples:
        print('existing sample - skipping...')
        continue
    if words_set == {"" for _ in range(16)}:
        print('dumping corrupted examples...') 
        continue
    
    samples.append(output)
    idx += 1



with open(output_path, 'w') as file:
    json.dump(samples, file, indent=4)