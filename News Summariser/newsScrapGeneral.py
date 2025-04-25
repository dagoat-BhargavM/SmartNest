import requests
from bs4 import BeautifulSoup
import csv
import re

# Define the ticker symbol and URL
ticker = "ZOMATO"
query = f"{ticker}"
url = f"https://www.google.com/search?q={query}&tbm=nws"

# Set headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Make the request and parse HTML
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Regex pattern for filtering today's news
time_pattern = re.compile(r"\b\d+\s+(minutes?|mins?|hours?)\s+ago\b", re.IGNORECASE)

# Extract article elements (multiple formats used by Google)
article_blocks = soup.find_all("a", href=True)

# Store news items
news_data = []

for tag in article_blocks:
    parent_text = tag.find_parent().get_text(" ", strip=True)

    # Match only today's items
    time_match = time_pattern.search(parent_text)
    if time_match:
        title = tag.get_text(strip=True)
        link = tag["href"]

        # Skip blank or unrelated titles
        if title and "google.com" not in link:
            news_data.append([ticker, title, link, time_match.group(0)])

# Save to CSV
csv_filename = f"{ticker}_news_today.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Ticker", "Title", "Link", "Time Published"])
    writer.writerows(news_data)

print(f"✅ Saved {len(news_data)} news articles from today to {csv_filename}")