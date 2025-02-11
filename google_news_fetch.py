# import requests
# import xml.etree.ElementTree as ET

# def fetch_google_news_rss(stock_name):
#     rss_url = f"https://news.google.com/rss/search?q={stock_name}+stock&hl=en-IN&gl=IN&ceid=IN:en"
#     response = requests.get(rss_url)
    
#     if response.status_code == 200:
#         root = ET.fromstring(response.content)
#         news_items = []
        
#         for item in root.findall(".//item"):
#             title = item.find("title").text
#             link = item.find("link").text
#             pub_date = item.find("pubDate").text
#             news_items.append({"title": title, "link": link, "pub_date": pub_date})
        
#         return news_items
#     else:
#         print("Failed to fetch RSS feed.")
#         return []

# # Example usage
# stock_name = input("Enter the stock name: ")
# news = fetch_google_news_rss(stock_name)
# if news:
#     print("\nTop News Articles:")
#     for idx, item in enumerate(news, start=1):
#         print(f"{idx}. {item['title']}\n   Link: {item['link']}\n   Published: {item['pub_date']}\n")
# else:
#     print("No news articles found.")


# import requests
# import xml.etree.ElementTree as ET
# from datetime import datetime

# def fetch_google_news_rss(stock_name):
#     rss_url = f"https://news.google.com/rss/search?q={stock_name}+stock&hl=en-IN&gl=IN&ceid=IN:en"
#     response = requests.get(rss_url)
    
#     if response.status_code == 200:
#         root = ET.fromstring(response.content)
#         news_items = []
        
#         for item in root.findall(".//item"):
#             title = item.find("title").text
#             link = item.find("link").text
#             pub_date = item.find("pubDate").text
#             # Parse the publication date
#             pub_date_parsed = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
#             news_items.append({"title": title, "link": link, "pub_date": pub_date, "pub_date_parsed": pub_date_parsed})
        
#         # Sort articles by publication date (latest first)
#         sorted_news_items = sorted(news_items, key=lambda x: x["pub_date_parsed"], reverse=True)
        
#         # Return only the top 10 articles
#         return sorted_news_items[:10]
#     else:
#         print("Failed to fetch RSS feed.")
#         return []

# # Example usage
# stock_name = input("Enter the stock name: ")
# news = fetch_google_news_rss(stock_name)
# if news:
#     print("\nTop 10 Latest News Articles:")
#     for idx, item in enumerate(news, start=1):
#         print(f"{idx}. {item['title']}\n   Link: {item['link']}\n   Published: {item['pub_date']}\n")
# else:
#     print("No news articles found.")


#/Users/bhargav/Downloads/Capstone Project/EQUITY_L.csv




import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import time
import os

# Function to fetch latest news for a stock (sorted by latest first)
def fetch_google_news_rss(stock_name):
    """Fetch latest Google News RSS feed for a given stock."""
    rss_url = f"https://news.google.com/rss/search?q={stock_name}+stock&hl=en-IN&gl=IN&ceid=IN:en"
    response = requests.get(rss_url)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        news_items = []
        
        for item in root.findall(".//item"):
            title = item.find("title").text
            link = item.find("link").text
            pub_date = item.find("pubDate").text
            
            # Parse publication date
            pub_date_parsed = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
            news_items.append({
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "pub_date_parsed": pub_date_parsed
            })
        
        # Sort by latest publication date
        sorted_news_items = sorted(news_items, key=lambda x: x["pub_date_parsed"], reverse=True)
        
        # Return only the top 10 latest articles
        return sorted_news_items[:10]
    else:
        print(f"⚠️ Failed to fetch news for {stock_name}")
        return []

# Load stock names from the first column of the uploaded CSV file
csv_file = "/Users/bhargav/Downloads/Capstone Project/EQUITY_L.csv"  # Update with your actual file path
stock_df = pd.read_csv(csv_file)

# Ensure the first column is used for stock names
stock_names = stock_df.iloc[:, 0].dropna().tolist()

# Overwrite existing CSV (create a fresh file)
stored_links_file = "new_stock_links.csv"

# Create a new CSV file with headers
with open(stored_links_file, "w") as f:
    f.write("Stock,Links,Latest Pub Date\n")

# Process stocks one by one and save immediately
for stock in stock_names:
    print(f"\n🔍 Fetching latest news for: {stock}")
    latest_news = fetch_google_news_rss(stock)
    
    if latest_news:
        # Extract new links and latest publication date
        new_links = ", ".join([item["link"] for item in latest_news])
        latest_pub_date = latest_news[0]["pub_date"]  # Store the latest news timestamp
        
        # Save immediately to CSV
        new_entry = pd.DataFrame([{"Stock": stock, "Links": new_links, "Latest Pub Date": latest_pub_date}])
        new_entry.to_csv(stored_links_file, mode="a", index=False, header=False)
        
        print(f"✅ {len(latest_news)} latest articles saved for {stock}")

    # time.sleep(2)  # Add a delay to avoid request limits

print("\n🚀 All stocks processed successfully! New CSV file updated in real-time.")
