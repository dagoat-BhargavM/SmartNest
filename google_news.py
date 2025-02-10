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


import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def fetch_google_news_rss(stock_name):
    rss_url = f"https://news.google.com/rss/search?q={stock_name}+stock&hl=en-IN&gl=IN&ceid=IN:en"
    response = requests.get(rss_url)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        news_items = []
        
        for item in root.findall(".//item"):
            title = item.find("title").text
            link = item.find("link").text
            pub_date = item.find("pubDate").text
            # Parse the publication date
            pub_date_parsed = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
            news_items.append({"title": title, "link": link, "pub_date": pub_date, "pub_date_parsed": pub_date_parsed})
        
        # Sort articles by publication date (latest first)
        sorted_news_items = sorted(news_items, key=lambda x: x["pub_date_parsed"], reverse=True)
        
        # Return only the top 10 articles
        return sorted_news_items[:10]
    else:
        print("Failed to fetch RSS feed.")
        return []

# Example usage
stock_name = input("Enter the stock name: ")
news = fetch_google_news_rss(stock_name)
if news:
    print("\nTop 10 Latest News Articles:")
    for idx, item in enumerate(news, start=1):
        print(f"{idx}. {item['title']}\n   Link: {item['link']}\n   Published: {item['pub_date']}\n")
else:
    print("No news articles found.")
