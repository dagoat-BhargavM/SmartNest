import os
import pandas as pd
from datetime import datetime
import time
import requests
import trafilatura
from readability import Document
from bs4 import BeautifulSoup
from newspaper import Article
import google.generativeai as genai

# 🔐 Gemini API key
genai.configure(api_key="AIzaSyAk-nJQftmcaVpg2j9DwCD0czr43ZvcGsg")
model = genai.GenerativeModel("gemini-1.5-flash")

# 📁 Paths
DAILY_CSV_PATH = "daily_sector_news"
DAILY_SUMMARY_PATH = "daily_sector_summary"
today_str = datetime.now().strftime("%Y-%m-%d")
os.makedirs(DAILY_SUMMARY_PATH, exist_ok=True)

# 📄 Load today's news CSV
csv_filename = f"sector_news_{today_str}.csv"
csv_path = os.path.join(DAILY_CSV_PATH, csv_filename)
df = pd.read_csv(csv_path)
sector_groups = df.groupby("Sector")

# 🧠 Multi-method article text extractor
def fetch_article_text(url, title):
    headers = {"User-Agent": "Mozilla/5.0"}

    # 1️⃣ Try trafilatura
    try:
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code == 200:
            text = trafilatura.extract(response.text, include_comments=False, include_tables=True)
            if text:
                print(f"[INFO] ✅ Traf extracted {len(text)} chars: {title}")
                return text.strip()
            else:
                print(f"[WARN] Traf failed (empty): {title}")
        else:
            print(f"[WARN] ❌ HTTP {response.status_code}: {title}")
    except Exception as e:
        print(f"[ERROR] Traf exception: {title} → {e}")

    # 2️⃣ Fallback: readability-lxml
    try:
        html = response.text
        doc = Document(html)
        clean_html = doc.summary()
        soup = BeautifulSoup(clean_html, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        if text:
            print(f"[INFO] 📖 Readability fallback used: {title}")
            return text
        else:
            print(f"[WARN] Readability returned empty: {title}")
    except Exception as e:
        print(f"[ERROR] Readability failed: {title} → {e}")

    # 3️⃣ Final fallback: newspaper3k
    try:
        article = Article(url)
        article.download()
        article.parse()
        if article.text:
            print(f"[INFO] 🧪 Newspaper3k fallback used: {title}")
            return article.text.strip()
        else:
            print(f"[WARN] Newspaper3k empty: {title}")
    except Exception as e:
        print(f"[ERROR] Newspaper3k failed: {title} → {e}")

    return ""

# 📊 Summarize sector news
def summarize_sector(sector, rows):
    enriched_news = []
    raw_text_dump = []

    for _, row in rows.iterrows():
        title = row["Title"]
        time_str = row["Time"]
        link = row["Link"]
        body = fetch_article_text(link, title)

        news_item = f"- {title} ({time_str})\nLink: {link}"
        raw_item = f"{title}\n{link}\n{body}\n\n" if body else f"{title}\n{link}\n[No text extracted]\n\n"

        enriched_news.append(news_item + ("\n\nBody:\n" + body if body else ""))
        raw_text_dump.append(raw_item)

    news_content = "\n\n".join(enriched_news)
    raw_text_combined = "".join(raw_text_dump)

    prompt = f"""You are a financial analyst summarizing daily sectoral news.

Here are today's ({today_str}) top news items for the "{sector}" sector in India:

{news_content}

Instructions:
- Write a 3–5 sentence summary using analytical, concise language.
- Capture key developments, sentiment, policy changes, and investment implications.
- Focus on today’s news only. Do not include raw URLs in your summary.

Begin your summary with: "**{sector} – {today_str}:**"
"""

    response = model.generate_content(prompt)
    time.sleep(5)
    return raw_text_combined, response.text.strip()

# 💾 Write summaries
for sector, group in sector_groups:
    raw_text, summary = summarize_sector(sector, group)
    safe_sector = sector.replace(" ", "_").replace("/", "_")
    sector_dir = os.path.join(DAILY_SUMMARY_PATH, safe_sector)
    os.makedirs(sector_dir, exist_ok=True)

    with open(os.path.join(sector_dir, f"{today_str}.txt"), "w", encoding="utf-8") as f:
        f.write(raw_text + "\n\n" + summary)
