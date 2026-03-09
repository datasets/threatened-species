import os
import sys

import pandas as pd
import requests

API_ENDPOINT = "https://apiv3.iucnredlist.org/api/v3"
TOKEN = os.getenv("IUCNREDLIST_TOKEN")
TIMEOUT_SECONDS = 60


def fetch_page(page: int) -> list[dict]:
    response = requests.get(
        f"{API_ENDPOINT}/species/page/{page}",
        params={"token": TOKEN},
        timeout=TIMEOUT_SECONDS,
    )
    print(f"Page {page} status code: {response.status_code}")
    response.raise_for_status()

    payload = response.json()
    if "result" not in payload:
        raise RuntimeError(f"Missing result field on page {page}: {payload}")

    return payload["result"]


def main() -> int:
    if not TOKEN:
        raise RuntimeError("IUCNREDLIST_TOKEN is not set")

    page = 1
    all_results = []

    while True:
        results = fetch_page(page)
        if not results:
            break

        all_results.extend(results)
        page += 1

    if not all_results:
        raise RuntimeError("No species data returned; refusing to overwrite dataset")

    df = pd.DataFrame(all_results)
    df.to_csv("data/threatened-species.csv", index=False)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Dataset update failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
