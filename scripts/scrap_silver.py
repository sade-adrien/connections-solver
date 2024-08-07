"""
This script scrapes samples from https://www.connectionsunlimited.org/ which provides unlimited (?) examples.
They are not from the original game and we're unsure about the method of creation or their quality in regards to the original game. We qualify those examples as silver.
This framework provides a level of difficulty: we select 1.5k easy samples, 3k medium and 1.5k hard.
"""

# from playwright.sync_api import sync_playwright

# # The words a
# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()

import requests
from bs4 import BeautifulSoup as bs

r = requests.get('https://www.connectionsunlimited.org/')

with open('test.txt', 'w') as f:
    f.write(str(r.content))