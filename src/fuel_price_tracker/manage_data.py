import urllib
from bs4 import BeautifulSoup
import requests
import os

url = "https://www.data.gouv.fr/fr/datasets/prix-des-carburants-en-france/"

if os.listdir("../../data/"):
    for item in os.listdir("../../data/"):
        os.remove(f"../../data/{item}")
page = requests.get(url)
if page.status_code == 200:
    soup = BeautifulSoup(page.text, "lxml")
    # print(soup.find_all(attrs={"class": "btn btn-sm btn-primary"}))
    links = [
        item.attrs for item in soup.find_all(attrs={"class": "btn btn-sm btn-primary"})
    ]
    links = [link["href"] for link in links if "href" in link.keys()]
os.makedirs("../../data", exist_ok=True)
urllib.request.urlretrieve(links[1], "../../data/price.zip")

import zipfile

with zipfile.ZipFile("../../data/price.zip", "r") as zip_ref:
    zip_ref.extractall("../../data/")
