import requests
from scihub import SciHub
import json
from config import SCOPUS_API_KEY, SCOPUS_API_ENDPOINT

query = SCOPUS_API_ENDPOINT + "?query=TITLE-ABS-KEY(bioprinting)&count=10&sort=+orig-load-date&date=2004-2010"

resp = requests.get(query,
                    headers={'Accept':'application/json',
                             'X-ELS-APIKey': SCOPUS_API_KEY})

dois = []
for i in resp.json()["search-results"]["entry"]:
    try:
        dois.append(i["prism:doi"])
    except:
        continue

print(dois)
SciHub(dois)

