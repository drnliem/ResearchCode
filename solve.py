import cloudscraper
from bs4 import BeautifulSoup
import csv
import time
import random

# buat cloudscraper
scraper = cloudscraper.create_scraper()  

# file input
with open("link2023.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f.readlines() if line.strip()]

# file output csv
output_file = "cnn2023_scraped.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["url", "title", "content"])

    for idx, url in enumerate(urls, 1):
        print(f"[{idx}/{len(urls)}] Scraping: {url}")

        try:
            # request
            r = scraper.get(url, timeout=15)

            # jika kena cloudflare
            if "Attention Required" in r.text or r.status_code != 200:
                print("⚠ Gagal (Cloudflare)")
                writer.writerow([url, "CLOUDFLARE BLOCKED", ""])
                continue

            soup = BeautifulSoup(r.text, "html.parser")

            # ambil title
            title = soup.find("title").get_text(strip=True) if soup.find("title") else ""

            # ambil isi berita 
            paragraphs = soup.find_all("p")
            content = "\n".join([p.get_text(strip=True) for p in paragraphs])

            writer.writerow([url, title, content])

            time.sleep(random.uniform(1.5, 3.7))

        except Exception as e:
            print("Error:", e)
            writer.writerow([url, "ERROR", ""])
            continue

print("Hasil tersimpan di:",output_file)