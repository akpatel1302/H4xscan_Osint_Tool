# 🔍 OSINT Intelligence Toolkit - **H4xscan By Ayush Patel ( H4xs13 )**

**H4xscan** is a modular, menu-driven OSINT (Open Source Intelligence) toolkit designed to extract, analyze, and export intelligence based on usernames and domains. It integrates social media enumeration, Google/DuckDuckGo dorking, DNS record lookups, subdomain discovery, and Instagram scraping — all from a single interface.

---

## 📌 Key Features

- 🎯 **Social Media Username Checker**
  - Searches Instagram, Facebook, Reddit, and Medium for user presence
  - Smart validation to avoid false positives

- 🌐 **Google & DuckDuckGo Dorking**
  - Uses dorking techniques to gather indexed intelligence
  - Queries customized for usernames and profiles

- 📸 **Instagram Scraper**
  - Fetches public Instagram user data using official APIs (no login required)

- 🧠 **DNS Record Lookup**
  - Retrieves A, MX, NS, CNAME, TXT, SOA, AAAA, SRV, PTR, and CAA records

- 🌐 **Subdomain Scanner**
  - Discovers valid subdomains using a wordlist and HTTP check

- 📤 **Export Results**
  - Saves output in JSON format for further analysis or automation

---

## 📂 Folder Structure

```
H4xscan/
├── output/                    # Exported JSON result files
├── subdomain_names.txt       # Wordlist for subdomain enumeration
├── main.py                   # Main application file
└── README.md                 # This file
```

---

## 🛠️ Installation

### ⚙️ Requirements

- Python 3.8+
- pip (Python package manager)

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt`:

```
requests
httpx
dnspython
beautifulsoup4
duckduckgo-search
```

---

## 🚀 Usage

### Run the tool

```bash
python main.py
```

### Menu Options

```

 _   _   ___                          
| | | | /   |                         
| |_| |/ /| |_  _____  ___ __ _ _ __  
|  _  / /_| \ \/ / __|/ __/ _` | '_ \ 
| | | \___  |>  <\__ \ (_| (_| | | | |
\_| |_/   |_/_/\_\___/\___\__,_|_| |_|
                                      
                                      
1. Social Media Username Checker
2. Instagram User Scraper
3. DNS Record Lookup
4. Subdomain Finder
5. Exit
```

---

## 🧪 Example Scenarios

- ✅ **Check if a username exists across multiple platforms**
- 📁 **Export discovered profiles to JSON**
- 🕸️ **Fetch indexed links using OSINT dorking**
- 🌐 **Scrape Instagram user metadata**
- 📡 **Run DNS queries and detect misconfigured records**
- 🔍 **Discover hidden subdomains**

---

## 📤 Exporting Results

After any module execution, you'll be prompted to export the results.

JSON files are saved under the `output/` directory:
```
output/social_media_<username>.json
output/instagram_<username>.json
output/dns_<domain>.json
output/subdomains_<domain>.json
```

---

## ⚠️ Disclaimer

This tool is developed **for educational and ethical use only**. Any misuse or illegal use is strictly discouraged. Always ensure you have permission before scanning or scraping data from external domains or platforms.

---

## 🙌 Contributing

Pull requests and suggestions are welcome! If you encounter bugs or have enhancement ideas, feel free to open an issue or fork the repository.

---


## 👨‍💻 Author

Made by **H4xs13 ( Ayush Patel )**


[![GitHub](https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/akpatel1302)  
[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@h4xs13)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/ayush-k-patel)

