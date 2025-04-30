import requests
import json
import httpx
import dns.resolver
from bs4 import BeautifulSoup
import os
import time
from duckduckgo_search import DDGS
import re


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def ensure_output_dir():
    if not os.path.exists("output"):
        os.makedirs("output")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (like osint) Chrome/62.0.3202.94 Safari/537.36"
}

SOCIAL_URLS = {
    "Instagram": "https://www.instagram.com/{}",
    "Facebook": "https://www.facebook.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Medium": "https://medium.com/@{}",
}

# def duckduckgo_dork(query, num_results=10):
#     print(f"\n[🔎] DuckDuckGo Dorking: {query}")
#     results = []
#     try:
#         url = "https://html.duckduckgo.com/html"
#         data = {"q": query}
#         r = requests.post(url, headers=headers, data=data, timeout=10)
#         soup = BeautifulSoup(r.text, "html.parser")
#         links = soup.find_all("a", class_="result__url", limit=num_results)
#         for link in links:
#             href = link.get("href")
#             if href:
#                 results.append(href)
#     except Exception as e:
#         print(f"[!] DuckDuckGo error: {e}")
#     return results

def duckduckgo_dork(query, num_pages=5, delay=2):
    print(f"\n[🔎] DuckDuckGo Dorking: {query}")
    results = []
    try:
        base_url = "https://html.duckduckgo.com/html"
        for page in range(num_pages):
            params = {
                "q": query,
                "s": str(page * 30)  # DuckDuckGo pagination step
            }
            r = requests.post(base_url, headers=headers, data=params, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            links = soup.find_all("a", class_="result__url")
            for link in links:
                href = link.get("href")
                if href and href not in results:
                    results.append(href)
            time.sleep(delay)  # Delay to avoid rate limiting
    except Exception as e:
        print(f"[!] DuckDuckGo error: {e}")
    return results

def google_dork(query, num_results=10):
    print(f"\n[🔎] Google Dorking: {query}")
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=num_results):
                results.append(r['href'])
    except Exception as e:
        print(f"[!] Google Dork error: {e}")
    return results


def check_username_on_sites(username):
    print("\n==== 🔎 Checking Social Media Platforms ====")
    found_accounts = {}

    for platform, url in SOCIAL_URLS.items():
        profile_url = url.format(username)
        try:
            res = requests.get(profile_url, headers=headers, timeout=10)

            if platform == "Instagram":
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    if "Sorry, this page isn't available." in res.text:
                        print(f"[✘] {platform}: Not found")
                    elif soup.find("meta", property="og:type") and "profile" in soup.find("meta", property="og:type")["content"]:
                        print(f"[✔] {platform}: Found ({profile_url})")
                        found_accounts[platform] = profile_url
                    else:
                        print(f"[✘] {platform}: Not found")
                else:
                    print(f"[✘] {platform}: Not found")

            elif platform == "Facebook":
                if res.status_code == 200 and res.text.strip():
                    try:
                        soup = BeautifulSoup(res.text, 'html.parser')
                        page_text = soup.get_text().lower()
                        if "page isn't available" in page_text or "content not found" in page_text or "log in to facebook" in page_text:
                            print(f"[✘] {platform}: Not found")
                        elif username.lower() in page_text:
                            print(f"[✔] {platform}: Found ({profile_url})")
                            found_accounts[platform] = profile_url
                        else:
                            print(f"[✘] {platform}: Not found")
                    except Exception as e:
                        print(f"[!] Error parsing Facebook page: {e}")
                else:
                    print(f"[✘] {platform}: Not found")

            elif platform == "Reddit":
                if res.status_code == 200 and f"/user/{username}" in res.url:
                    soup = BeautifulSoup(res.text, "html.parser")
                    if soup.find("h1") and "Sorry" in soup.find("h1").text:
                        print(f"[✘] {platform}: Not found")
                    else:
                        print(f"[✔] {platform}: Found ({profile_url})")
                        found_accounts[platform] = profile_url
                else:
                    print(f"[✘] {platform}: Not found")

            elif platform == "Medium":
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, "html.parser")
                    page_text = soup.get_text().lower()

                    if "404 - not found" in page_text or "page not found" in page_text or "out of nothing, something." in page_text:
                        print(f"[✘] {platform}: Not found")
                    else:
                        print(f"[✔] {platform}: Found ({profile_url})")
                        found_accounts[platform] = profile_url
                else:
                    print(f"[✘] {platform}: Not found")

            else:
                print(f"[!] Unsupported platform: {platform}")

        except Exception as e:
            print(f"[!] Error checking {platform}: {e}")

    print("\n==== 🔎 Dorking for Social Media ====")
    dorks = [
        f'"{username}" site:instagram.com',
        f'"{username}" site:facebook.com',
        f'"{username}" site:reddit.com',
        f'"{username}" site:medium.com',
        f'"{username}" site:pastebin.com',
        f'"{username}" inurl:profile',
        f'"{username}" filetype:pdf'
    ]

    all_duckduckgo_results = []
    all_google_results = []

    # for q in dorks:
    #     duck_results = duckduckgo_dork(q)
    #     google_results = google_dork(q)
    #     all_duckduckgo_results.extend(duck_results)
    #     all_google_results.extend(google_results)
    #     time.sleep(1)

    for q in dorks:
        duck_results = duckduckgo_dork(q, num_pages=5)
        google_results = google_dork(q)  # Optional: keep or remove
        all_duckduckgo_results.extend(duck_results)
        all_google_results.extend(google_results)
        time.sleep(1)


    if all_duckduckgo_results:
        print("\n==== 🌐 DuckDuckGo Dorking Results ====")
        for url in all_duckduckgo_results:
            print(url)
    else:
        print("\n[!] No results from DuckDuckGo.")

    if all_google_results:
        print("\n==== 🌐 Google Dorking Results ====")
        for url in all_google_results:
            print(url)
    else:
        print("\n[!] No results from Google.")

    found_accounts["duckduckgo_results"] = all_duckduckgo_results
    found_accounts["google_results"] = all_google_results

    return found_accounts

#                       <-- changed the above code and below code remains same -->

def export_json(data, filename):
    ensure_output_dir()
    filepath = os.path.join("output", filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"[✓] Results exported to {filepath}\n")

def scrape_instagram_user(username):
    client = httpx.Client(
        headers={
            "x-ig-app-id": "936619743392459",
            "User-Agent": headers["User-Agent"],
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "*/*",
        }
    )
    try:
        result = client.get(f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}")
        data = json.loads(result.content)
        return data["data"]["user"]
    except Exception as e:
        print(f"[!] Instagram scraping failed: {e}")
        return {}

def is_valid_domain(domain):
    # Basic regex for domain validation
    pattern = r"^(?!\-)(?:[a-zA-Z0-9\-]{1,63}(?<!\-)\.)+[a-zA-Z]{2,}$"
    return re.match(pattern, domain) is not None
def get_records(domain):
    dns_records_array = [
        'A', 'NS', 'CNAME', 'SOA', 'PTR', 'MX', 'TXT', 'AAAA', 'SRV', 'CAA'
    ]
    found_records = {}

    for record_type in dns_records_array:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            found_records[record_type] = [r.to_text() for r in answers]
            for rdata in answers:
                print(f"{record_type}: {rdata.to_text()}")
        except Exception:
            pass
    return found_records

def domain_sub_domain_scanner(domain_name, sub_domnames):
    found = []
    for i, subdomain in enumerate(sub_domnames):
        url = f"https://{subdomain}.{domain_name}"
        print(f"[*] Checking {url} ({i + 1}/{len(sub_domnames)})")
        try:
            requests.get(url)
            print(f"[+] Found ✅: {url}")
            found.append(url)
        except requests.ConnectionError:
            pass
        time.sleep(0.1)
    return found

def main():
    while True:
        clear()
        print("""
==== 🕵️ OSINT TOOL MENU ====
1. Social Media Username Checker
2. Instagram User Scraper
3. DNS Record Lookup
4. Subdomain Finder
5. Exit
""")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter the username to check: ")
            results = check_username_on_sites(username)
            export = input("Export results? (y/n): ").lower()
            if export == 'y':
                export_json(results, f"social_media_{username}.json")

        elif choice == '2':
            username = input("Enter Instagram username: ")
            data = scrape_instagram_user(username)
            if data:
                print(json.dumps(data, indent=4))
                export = input("Export results? (y/n): ").lower()
                if export == 'y':
                    export_json(data, f"instagram_{username}.json")

        # elif choice == '3':
        #     domain = input("Enter domain for DNS lookup: ")
        #     records = get_records(domain)
        #     export = input("Export results? (y/n): ").lower()
        #     if export == 'y':
        #         export_json(records, f"dns_{domain}.json")

        elif choice == '3':
            domain = input("Enter domain for DNS lookup: ").strip()
            if not is_valid_domain(domain):
                print("[!] Invalid domain format. Please enter a valid domain like example.com.")
                input("Press Enter to return to menu...")
            else:
                records = get_records(domain)
                export = input("Export results? (y/n): ").lower()
                if export == 'y':
                    export_json(records, f"dns_{domain}.json")

        elif choice == '4':
            domain = input("Enter domain for subdomain scan: ")
            sub_file = input("Enter path to subdomain list file (e.g., subdomain_names.txt): ")
            try:
                with open(sub_file, 'r') as f:
                    subdomains = f.read().splitlines()
                found = domain_sub_domain_scanner(domain, subdomains)
                export = input("Export results? (y/n): ").lower()
                if export == 'y':
                    export_json({i: url for i, url in enumerate(found)}, f"subdomains_{domain}.json")
            except FileNotFoundError:
                print("[!] Subdomain list file not found.")
                input("Press Enter to continue...")

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")
        input("\nPress Enter to return to menu...")

if __name__ == '__main__':
    main()
