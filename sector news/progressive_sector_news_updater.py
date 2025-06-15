import os
from datetime import datetime
import google.generativeai as genai
import time

# 🔐 Gemini API key
genai.configure(api_key="AIzaSyAk-nJQftmcaVpg2j9DwCD0czr43ZvcGsg")
model = genai.GenerativeModel("gemini-1.5-flash")

# 📂 Paths
DAILY_DIR = "daily_sector_summary"
PROGRESSIVE_DIR = "progressive_sector_news"
today_str = datetime.now().strftime("%Y-%m-%d")

os.makedirs(PROGRESSIVE_DIR, exist_ok=True)

# 🧠 Extract last block as summary from .txt
def extract_daily_summary(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
            last_block = text.split("\n\n")[-1]
            return last_block
    except Exception as e:
        print(f"⚠️ Error reading daily summary: {file_path} — {e}")
        return ""

# 🔁 Safe Gemini wrapper with retry
def safe_generate(prompt, retries=3, delay=30):
    for attempt in range(1, retries + 1):
        try:
            response = model.generate_content(prompt)
            return response
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                print(f"[RATE LIMIT] Attempt {attempt}/{retries}. Sleeping for {delay}s...")
                time.sleep(delay)
            else:
                print(f"[ERROR] Unexpected failure: {e}")
                break
    print("❌ All retries failed. Skipping.")
    return None

# 🧠 Progressive summarization using Gemini
def update_progressive_summary(sector, prev_summary, daily_summary):
    prompt = f"""You are a senior financial analyst maintaining a progressive news summary.

Here is the current progressive summary for the "{sector}" sector:

{prev_summary}

Here is today's update ({today_str}):

{daily_summary}

Integrate the new insights into the existing summary. Avoid repetition. Maintain a structured, analytical tone. Start with "**{sector} Sector – Updated Summary:**"
"""

    response = safe_generate(prompt)
    if response:
        return response.text.strip()
    else:
        return prev_summary  # fallback to old summary if failure

# 🔄 Process each sector folder
for sector_folder in os.listdir(DAILY_DIR):
    sector_path = os.path.join(DAILY_DIR, sector_folder)
    daily_file = os.path.join(sector_path, f"{today_str}.txt")

    if not os.path.exists(daily_file):
        print(f"⏭️ Skipping {sector_folder}, no daily file found.")
        continue

    daily_summary = extract_daily_summary(daily_file)
    progressive_file = os.path.join(PROGRESSIVE_DIR, f"{sector_folder}.txt")

    if os.path.exists(progressive_file):
        with open(progressive_file, "r", encoding="utf-8") as f:
            prev_summary = f.read().strip()
    else:
        prev_summary = f"# Progressive News Summary for {sector_folder}\n"

    updated = update_progressive_summary(sector_folder, prev_summary, daily_summary)

    with open(progressive_file, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"✅ Updated progressive summary for: {sector_folder}")
