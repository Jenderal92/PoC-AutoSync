import os
import requests
import json
import datetime

POCS_DIR = "pocs"

# Ambil data dari situs API
url = "https://poc-in-github.motikan2010.net/api/v1/?per_page=100"
print("[*] Fetching data from:", url)

response = requests.get(url)
data = response.json()

# Cek struktur data
for k in ('pocs', 'results', 'items'):
    if k in data:
        data = data[k]
        break

if not isinstance(data, list):
    print("[-] Unexpected data structure")
    exit(1)

# Buat folder output
if not os.path.exists(POCS_DIR):
    os.makedirs(POCS_DIR)

# Tulis setiap PoC ke file
today = datetime.date.today().isoformat()
output_file = os.path.join(POCS_DIR, f"pocs_{today}.json")

with open(output_file, "w") as f:
    json.dump(data, f, indent=2)

print("[+] Saved:", output_file)
print("[+] Total entries:", len(data))
