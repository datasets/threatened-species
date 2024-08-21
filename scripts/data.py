import os

import pandas as pd
import requests

API_ENDPOINT = "https://apiv3.iucnredlist.org/api/v3"
TOKEN = os.getenv("IUCNREDLIST_TOKEN")

page = 1
all_results = []

while True:
    r = requests.get(f"{API_ENDPOINT}/species/page/{page}?token={TOKEN}")
    print(f"Page {page} status code: {r.status_code}")

    if r.status_code != 200 or r.json()["result"] == []:
        break

    results = r.json()["result"]
    all_results.extend(results)
    page += 1

df = pd.DataFrame(all_results)

df.to_csv("data/threatened-species.csv", index=False)
