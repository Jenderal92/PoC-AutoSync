import os
import requests
import json
import datetime

POCS_DIR = "pocs"

def main():
    url = "https://poc-in-github.motikan2010.net/api/v1/?per_page=30"
    print("[*] Fetching data from:", url)
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("[-] Error fetching API:", e)
        exit(1)

    for k in ('pocs', 'results', 'items'):
        if k in data:
            data = data[k]
            break

    if not isinstance(data, list):
        print("[-] Unexpected data structure:", type(data))
        exit(1)

    if not os.path.exists(POCS_DIR):
        os.makedirs(POCS_DIR)

    today = datetime.date.today().isoformat()
    output_file = os.path.join(POCS_DIR, f"pocs_{today}.json")

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

    print("[+] Saved:", output_file)
    print("[+] Total entries:", len(data))

if __name__ == "__main__":
    main()
