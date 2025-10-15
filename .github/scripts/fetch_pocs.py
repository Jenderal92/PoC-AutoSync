import os
import requests
import json
import datetime

BASE_DIR = "pocs"

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

    # Adapt struktur JSON
    for k in ('pocs', 'results', 'items'):
        if k in data:
            data = data[k]
            break

    if not isinstance(data, list):
        print("[-] Unexpected data structure:", type(data))
        exit(1)

    # Buat folder berdasarkan tahun
    year = str(datetime.date.today().year)
    year_dir = os.path.join(BASE_DIR, year)
    if not os.path.exists(year_dir):
        os.makedirs(year_dir)

    today = datetime.date.today().isoformat()
    output_file = os.path.join(year_dir, f"pocs_{today}.json")

    # Cek duplikat: kalau file sudah ada, skip
    if os.path.exists(output_file):
        print("[=] File already exists, not recreated:", output_file)
        return

    # Simpan file baru
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

    print("[+] Saved:", output_file)
    print("[+] Total entries:", len(data))

if __name__ == "__main__":
    main()
