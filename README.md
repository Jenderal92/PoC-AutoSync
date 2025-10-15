# 🧠 PoC-AutoSync

Automatically collects public Proof-of-Concept (PoC) exploits from poc-in-github.motikan2010.net and keeps the database up to date with automatic updates. Use responsibly — for research and defensive purposes only.



#### Inspired by [nomi-sec/PoC-in-GitHub](https://github.com/nomi-sec/PoC-in-GitHub).

---

## 🔍 Overview

This repository is updated automatically via GitHub Actions every hour.

Each CVE PoC is stored as a Markdown file in the `/pocs/` directory.  
Each file contains metadata such as CVE ID, repository link, stars, and descriptions.

---

## ⚙️ How It Works

1. Fetches the latest PoC list from `https://poc-in-github.motikan2010.net/api/v1/`.
2. Compares existing files in `/pocs/`.
3. Creates new `.md` files for PoCs that are not yet included.
4. Opens a Pull Request with all new PoCs.

---

## 📅 Update Schedule
- Automatically runs **every hour** via GitHub Actions.
- You can manually trigger updates under the “Actions” tab.

---

## 🧩 Credits
- Data Source: [poc-in-github.motikan2010.net](https://poc-in-github.motikan2010.net)
- Inspired by: [nomi-sec/PoC-in-GitHub](https://github.com/nomi-sec/PoC-in-GitHub)
- Maintainer: [@Jenderal92](https://github.com/Jenderal92)

---

## 📜 License
MIT License
