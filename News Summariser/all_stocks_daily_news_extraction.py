# import requests
# from bs4 import BeautifulSoup
# import csv
# import re
# import pandas as pd
# import time
# import random

# # Load tickers from the uploaded CSV
# df = pd.read_csv("EQUITY_L.csv")
# tickers = df['SYMBOL'].dropna().unique().tolist()

# # Regex pattern to filter only today's news
# time_pattern = re.compile(r"\b\d+\s+(minutes?|mins?|hours?)\s+ago\b", re.IGNORECASE)

# # Set headers to mimic a browser
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# }

# # CSV filename
# csv_filename = "all_stock_news_today.csv"

# # Create the CSV file and write header
# with open(csv_filename, "w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Ticker", "Title", "Link", "Time Published"])

# # Start scraping
# for idx, ticker in enumerate(tickers, 1):
#     query = f"{ticker} stock"
#     encoded_query = requests.utils.quote(query)
#     url = f"https://www.google.com/search?q={encoded_query}&tbm=nws"

#     articles_found = 0  # counter for this ticker

#     try:
#         response = requests.get(url, headers=headers)
#         soup = BeautifulSoup(response.text, "html.parser")

#         article_blocks = soup.find_all("a", href=True)

#         with open(csv_filename, "a", newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)

#             for tag in article_blocks:
#                 parent_text = tag.find_parent().get_text(" ", strip=True)

#                 # Filter only today's news
#                 time_match = time_pattern.search(parent_text)
#                 if time_match:
#                     title = tag.get_text(strip=True)
#                     link = tag["href"]

#                     if title and "google.com" not in link:
#                         writer.writerow([ticker, title, link, time_match.group(0)])
#                         articles_found += 1

#         print(f"[{idx}/{len(tickers)}] ✅ {ticker}: {articles_found} article(s) saved.")
#         time.sleep(random.uniform(1, 4))

#     except Exception as e:
#         print(f"[{idx}/{len(tickers)}] ❌ Error fetching news for {ticker}: {e}")

# print(f"\n🎉 Done! All results saved in: {csv_filename}")





import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
import time
import random

# Load tickers from the uploaded CSV
df = pd.read_csv("EQUITY_L.csv")
tickers = df['SYMBOL'].dropna().unique().tolist()

# Regex pattern to filter only today's news
time_pattern = re.compile(r"\b\d+\s+(minutes?|mins?|hours?)\s+ago\b", re.IGNORECASE)

# Set headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# CSV filename
csv_filename = "all_stock_news_today.csv"

# Create the CSV file and write header
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Ticker", "Title", "Link", "Time Published"])

# Start scraping
for idx, ticker in enumerate(tickers, 1):
    query = f"{ticker} stock"
    encoded_query = requests.utils.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}&tbm=nws"

    articles_found = 0  # counter for this ticker

    try:
        response = requests.get(url, headers=headers)

        # Rate limit or CAPTCHA detection
        if "unusual traffic" in response.text.lower() or "detected unusual traffic" in response.text.lower():
            print("🚫 Google has flagged your request as unusual traffic. You may be rate-limited or blocked.")
            print(f"⏹️ Stopping at ticker #{idx}: {ticker}")
            exit()

        soup = BeautifulSoup(response.text, "html.parser")
        article_blocks = soup.find_all("a", href=True)

        with open(csv_filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for tag in article_blocks:
                parent_text = tag.find_parent().get_text(" ", strip=True)

                # Filter only today's news
                time_match = time_pattern.search(parent_text)
                if time_match:
                    title = tag.get_text(strip=True)
                    link = tag["href"]

                    if title and "google.com" not in link:
                        writer.writerow([ticker, title, link, time_match.group(0)])
                        articles_found += 1

        print(f"[{idx}/{len(tickers)}] ✅ {ticker}: {articles_found} article(s) saved.")
        # time.sleep(random.uniform(1, 3))

    except Exception as e:
        print(f"[{idx}/{len(tickers)}] ❌ Error fetching news for {ticker}: {e}")

print(f"\n🎉 Done! All results saved in: {csv_filename}")
