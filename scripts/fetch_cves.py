import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

OUTPUT_DIR = Path("corpus/cve")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SEARCH_QUERIES = ["SQL Injection Python", "cross site scripting JavaScript", "deserialization Python", "authentication bypass Python",]

def fetch_cvss(keyword: str, limit: int = 5):
    headers = {}

    api_key = os.getenv("NVD_API_KEY")

    if api_key:
        headers["apiKey"] = api_key

    params = {"keywordSearch": keyword, "resultsPerPage": limit}

    response = requests.get(NVD_API_URL, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    return response.json().get("vulnerabilities", [])

def extract_cvss(cve: dict):
    metrics = cve.get("metrics", {})

    for metric_name in ("cvssMetricV31", "cvssMetricV30", "cvssMerticV2"):
        metrics_list = metrics.get(metric_name)

        if not metrics_list:
            continue

        first_metric = metrics_list[0]
        cvss_data = first_metric.get("cvssData", {})

        score = cvss_data.get("baseScore")

        if score is not None:
            return score

    return None

def save_cve(cve: dict):

    cve_id = cve.get("id")

    descriptions = cve.get("descriptions", [])

    description = ""

    for item in descriptions:
        if item.get("lang") == "en":
            description = item.get("value", "")
            break

    cvss_score = extract_cvss(cve)

    data = {
        "cve_id": cve_id,
        "description": description,
        "cvss_score": cvss_score,
        "source":  f"https://nvd.nist.gov/vuln/detail/{cve_id}",
        "doc_type": "cve"
    }

    output_path = OUTPUT_DIR / f"{cve_id}.json"

    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) , encoding="utf-8")

    print(f"Saved {cve_id}" f"(CVSS {cvss_score})")

def main():
    saved = set()

    for query in SEARCH_QUERIES:
        print(f"\nSearching: {query}")

        results = fetch_cvss(query)

        for result in results:
            cve = result.get("cve")

            if not cve:
                continue

            cve_id = cve.get("id")

            if not cve_id:
                continue

            if cve_id in saved:
                continue

            cvss_score = extract_cvss(cve)

            if cvss_score is None:
                continue

            if cvss_score < 7.0:
                continue

            save_cve(cve)

            saved.add(cve_id)

            if len(saved) >= 8:
                print(f"\nCollected 8 CVEs")
                return

    print(f"\nOnly {len(saved)} CVEs found")

if __name__ == "__main__":
    main()