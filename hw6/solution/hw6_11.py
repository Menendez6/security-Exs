#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup

addr = sys.argv[1] if len(sys.argv) > 1 else "http://0.0.0.0:5001"

url = addr + "/messages"
payload = {'id': "fhriu' OR mail like 'james@bond.mi5"}
r = requests.get(url, payload)
soup = BeautifulSoup(r.text, "html.parser")
if "Server Error" in soup.text:
    print("Nope, that's an error")
else:
    for div in soup.find_all('div', {"class": "p-2 m-2 card"}):
        if "james" in div.text:
            for blockquote in div.find_all('blockquote'):
                print(blockquote.text)
