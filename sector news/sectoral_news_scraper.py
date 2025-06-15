import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import csv
import re
from urllib.parse import urlparse, parse_qs

# List of Indian sectors with corresponding search queries
SECTOR_KEYWORDS = {
    "Minerals & Mining": "Minerals and Mining sector India",
    "Capital Markets": "Capital Markets sector India",
    "IT - Software": "IT Software sector India",
    "Diversified": "Diversified business sector India",
    "Finance": "Finance sector India",
    "Construction": "Construction sector India",
    "Commercial Services & Supplies": "Commercial services and supplies India",
    "Oil": "Oil sector India",
    "Pharmaceuticals & Biotechnology": "Pharmaceuticals and biotechnology India",
    "Electrical Equipment": "Electrical equipment sector India",
    "Chemicals & Petrochemicals": "Chemicals and petrochemicals sector India",
    "Textiles & Apparels": "Textiles and apparels India",
    "Beverages": "Beverages sector India",
    "Retailing": "Retail sector India",
    "Paper, Forest & Jute Products": "Paper forest jute products India",
    "Cement & Cement Products": "Cement sector India",
    "Transport Services": "Transport services India",
    "Agricultural, Commercial & Construction Vehicles": "Agricultural and construction vehicles India",
    "Power": "Power sector India",
    "Metals & Minerals Trading": "Metals and minerals trading India",
    "Transport Infrastructure": "Transport infrastructure India",
    "Food Products": "Food products sector India",
    "Consumer Durables": "Consumer durables sector India",
    "Industrial Products": "Industrial products sector India",
    "IT - Services": "IT services sector India",
    "Leisure Services": "Leisure services sector India",
    "Gas": "Gas sector India",
    "Industrial Manufacturing": "Industrial manufacturing India",
    "Healthcare Services": "Healthcare services sector India",
    "Realty": "Real estate sector India",
    "Agricultural Food & other Products": "Agricultural food products India",
    "Fertilizers & Agrochemicals": "Fertilizers and agrochemicals India",
    "Financial Technology (Fintech)": "Fintech sector India",
    "Telecom -  Equipment & Accessories": "Telecom equipment sector India",
    "Auto Components": "Auto components sector India",
    "Household Products": "Household products India",
    "Ferrous Metals": "Ferrous metals sector India",
    "Consumable Fuels": "Consumable fuels sector India",
    "Aerospace & Defense": "Aerospace and defense India",
    "Other Consumer Services": "Consumer services sector India",
    "Automobiles": "Automobile sector India",
    "Banks": "Banking sector India",
    "Other Utilities": "Utility sector India",
    "Entertainment": "Entertainment sector India",
    "Personal Products": "Personal products sector India",
    "Non - Ferrous Metals": "Non-ferrous metals sector India",
    "Telecom - Services": "Telecom services India",
    "Petroleum Products": "Petroleum products India",
    "IT - Hardware": "IT hardware sector India",
    "Media": "Media sector India",
    "Engineering Services": "Engineering services India",
    "Other Construction Materials": "Construction materials sector India",
    "Insurance": "Insurance sector India",
    "Diversified FMCG": "Diversified FMCG sector India",
    "Cigarettes & Tobacco Products": "Cigarettes and tobacco India",
    "Printing & Publication": "Printing and publication India",
    "Healthcare Equipment & Supplies": "Healthcare equipment supplies India",
    "Diversified Metals": "Diversified metals sector India"
}


# Output setup
BASE_DIR = "daily_sector_news"
os.makedirs(BASE_DIR, exist_ok=True)
csv_filename = os.path.join(BASE_DIR, f"sector_news_{datetime.now().strftime('%Y-%m-%d')}.csv")
headers = {"User-Agent": "Mozilla/5.0"}
time_pattern = re.compile(r"(minutes?|hours?) ago", re.IGNORECASE)

# Initialize CSV file
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Sector", "Title", "Link", "Time"])

# Scraping loop
for idx, (sector, query) in enumerate(SECTOR_KEYWORDS.items(), 1):
    encoded_query = requests.utils.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}&tbm=nws"
    articles_found = 0

    try:
        response = requests.get(url, headers=headers)

        if "unusual traffic" in response.text.lower():
            print("🚫 Google blocked your request.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        article_blocks = soup.find_all("a", href=True)

        with open(csv_filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for tag in article_blocks:
                parent_text = tag.find_parent().get_text(" ", strip=True)

                if time_pattern.search(parent_text):
                    title = tag.get_text(strip=True)
                    raw_link = tag["href"]

                    # ✅ Extract actual article URL
                    if "/url?q=" in raw_link:
                        link = parse_qs(urlparse(raw_link).query).get("q", [""])[0]
                    else:
                        link = raw_link

                    if title and "google.com" not in link:
                        writer.writerow([sector, title, link, time_pattern.search(parent_text).group(0)])
                        articles_found += 1

        print(f"[{idx}/{len(SECTOR_KEYWORDS)}] ✅ {sector}: {articles_found} article(s) saved.")
        time.sleep(2)

    except Exception as e:
        print(f"[{idx}/{len(SECTOR_KEYWORDS)}] ❌ Error for {sector}: {e}")
