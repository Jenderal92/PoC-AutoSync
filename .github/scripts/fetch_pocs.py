#!/usr/bin/env python3
# .github/scripts/fetch_pocs.py
import os
import requests
import time
import json

API = os.environ.get('API_BASE', 'https://poc-in-github.motikan2010.net/api/v1/')
POCS_DIR = os.environ.get('POCS_DIR', 'pocs')
LIMIT = int(os.environ.get('LIMIT', 200))

def slugify_cve(cve):
    return cve.upper().strip().replace(' ', '-')

def filename_for(cve):
    return os.path.join(POCS_DIR, f"{slugify_cve(cve)}.md")

def fetch_pocs(limit=LIMIT):
    params = {'limit': limit}
    r = requests.get(API, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
      
        for k in ('pocs','results','items'):
            if k in data and isinstance(data[k], list):
                return data[k]

        for v in data.values():
            if isinstance(v, list):
                return v
        return []
    elif isinstance(data, list):
        return data
    return []

def make_markdown(poc):
    cve = poc.get('cve_id') or poc.get('name') or poc.get('full_name') or 'UNKNOWN'
    repo = poc.get('html_url') or poc.get('repo') or poc.get('full_name') or ''
    owner = poc.get('owner', '')
    desc = poc.get('description', '') or poc.get('summary', '')
    nvd = poc.get('nvd_description', '') or ''
    stars = poc.get('stargazers_count') or poc.get('stars') or ''
    created = poc.get('created_at') or poc.get('created') or ''
    updated = poc.get('updated_at') or poc.get('pushed_at') or ''

    md = f"""---
cve: "{cve}"
repo: "{repo}"
owner: "{owner}"
stars: "{stars}"
created_at: "{created}"
updated_at: "{updated}"
---

# {cve}

**Repository:** {repo}

**Owner:** {owner}  
**Stars:** {stars}  
**Created at:** {created}  
**Updated at:** {updated}

## Short description
{desc}

## NVD / vendor details
{nvd}

## Notes
- Source: poc-in-github.motikan2010.net API
- Fetched at: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC
"""
    return md

def main():
    os.makedirs(POCS_DIR, exist_ok=True)
    try:
        pocs = fetch_pocs()
    except Exception as e:
        print("ERROR fetching API:", e)
        return

    added = []
    for poc in pocs:
        cve = poc.get('cve_id') or poc.get('name') or poc.get('full_name')
        if not cve:
            continue
        fname = filename_for(cve)
        if os.path.exists(fname):
            continue
        md = make_markdown(poc)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(md)
        added.append(fname)
        print("Added:", fname)

    if not added:
        print("No new PoCs found.")
    else:
        print(f"Total new files: {len(added)}")
        # konfigurasi git untuk runner
        os.system('git config user.name "github-actions[bot]"')
        os.system('git config user.email "41898282+github-actions[bot]@users.noreply.github.com"')
        os.system(f'git add {POCS_DIR}')
        os.system('git commit -m "Add new PoC(s) from poc-in-github" || true')

if __name__ == "__main__":
    main()
