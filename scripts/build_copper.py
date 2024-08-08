"""
This script builds new examples from the golden and silver samples. This new examples will be new combinations of existing groups. 
We acknowledge that those examples are not introducing new comprehensive knowledge of the grouping but rather constitutes mass to help the model train.
We consider the quality of those examples rather poor (especially because we loose the relations between groups that make up the difficulty of the game) and we voluntarily limit their number: those are our copper examples.
To ensure diversity we draw without replacement, so that each sample chosen once is never chosen again (this naturally limit the number of created examples).
"""
import random as rd
import json

golden_path = 'data/connections_golden.json'
silver_path = 'data/connections_silver.json'
copper_path = 'data/connections_copper.json'

with open(golden_path, 'r') as file:
    golden_data = json.load(file)
with open(silver_path, 'r') as file:
    silver_data = json.load(file)


# Build all existing word groups from gold and silver samples
word_groups = []
for game in golden_data + silver_data:
    for d in game['data']:
        word_groups.append(
            (d['description'], d['words'])
        )

# Build the existing games to avoid duplication - even if unlikely
existing_games = []
for game in golden_data + silver_data:
    words_set = {word for item in game['data'] for word in item['words']}
    existing_games.append(words_set)


# Draw groups and build new games
copper = []
i = 1
while len(word_groups) > 0:
    new_game = {'idx': i, 'source':'manual build', 'data': []}
    for _ in range(4):
        idx = rd.randint(0, len(word_groups)-1)
        group = word_groups.pop(idx)
        new_game['data'].append(
            {
                'description': group[0],
                'words': group[1],
            }
        )
    
    words_set = {word for item in new_game['data'] for word in item['words']}
    if words_set in existing_games:
        print('existing sample - skipping...')
        continue
    
    copper.append(new_game)
    i += 1



with open(copper_path, 'w') as file:
    json.dump(copper, file, indent=4)