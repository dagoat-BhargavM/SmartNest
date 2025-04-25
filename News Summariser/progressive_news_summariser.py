import ssl
import re
import time
import nltk
import pandas as pd
from newspaper import Article
from nltk.tokenize import sent_tokenize
import requests
import json
from pymongo import MongoClient

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
print("Script is running\n")

client = MongoClient('mongodb+srv://bharath:bharath123@cluster0.eomf8rh.mongodb.net/prog_news?retryWrites=true&w=majority', tls=True, tlsAllowInvalidCertificates=True)
db = client['prog_news']
collection = db['stocks']


def clean_text(text):
    """
    Clean the extracted text by removing common advertising and boilerplate patterns.
    """
    ad_patterns = [
        r'advertisement',
        r'sponsored content',
        r'subscribe now',
        r'sign up for our newsletter',
        r'related articles',
        r'\[.?ad.?\]', 
        r'share this article',
        r'follow us on'
    ]
    print("Function clean_text called")
    cleaned_text = text
    for pattern in ad_patterns:
        cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)
    
    cleaned_text = '\n'.join(line.strip() for line in cleaned_text.split('\n') if line.strip())
    cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text)
    
    return cleaned_text

def extract_article_content(url):
    """
    Extracts and cleans article content from the given URL.
    """
    try:
        print("extract_article_content")
        print(f"Processing URL: {url}")
        article = Article(url)
        article.download()
        time.sleep(2) 
        article.parse()

        sentences = sent_tokenize(article.text)

        processed_text = '\n'.join(sentences)
        final_text = clean_text(processed_text)

        return {
            'title': article.title,
            'text': final_text,
            'authors': article.authors,
            'date': article.publish_date
        }
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return None

csv_file_path = 'BAJAJHFL_news_today.csv'
csv_file_path2 = 'BAJAJHFL_NSE_news_today.csv'

df = pd.read_csv(csv_file_path)
df2 = pd.read_csv(csv_file_path2)

#1 refers to generic news
#2 refers to NSE market related news

unique_stocks2 = df2["Ticker"].unique()

for stock_ticker in unique_stocks2:
    print(f"Extracting articles for {stock_ticker}...")

    df_filtered = df2[df2["Ticker"].str.upper() == stock_ticker.upper()]

    articles_content = []
    for index, row in df_filtered.iterrows():
        url = row["Link"]
        result = extract_article_content(url)
        
        if result:
            article_text = f"Title: {result['title']}\nAuthors: {', '.join(result['authors']) if result['authors'] else 'Unknown'}\nDate: {result['date'] if result['date'] else 'Unknown'}\n\n{result['text']}\nEOF"
            articles_content.append(article_text)

    combined_content = "\n\n".join(articles_content)

    print(f"Length of combined content for {stock_ticker}: {len(combined_content)}")
    print(f"First 500 characters of combined content:\n{combined_content[:100]}")  # Print first 500 characters for inspection

    analyst_summary = """
    Mimic the role of an experienced financial
    analyst and distill the stock's daily market related news and generate a concise daily news
    summary.
    Please structure the output exactly using the format provided below. 
    Keep the language analytical, concise, and factual. Do not add extra commentary or headings.
      
    📅 Date: [DD MMM YYYY]
    🏢 Company: [Company Name] ([Ticker Symbol])
    1. Stock-Specific News
    [Summarize key news directly impacting the stock price: earnings, market sentiment, product updates, etc.]

    [e.g., Apple stock rose 1.5'%' after strong earnings report.]

    2. Market Reaction & Trading Insights
    [Include price change, volume spikes, and any notable market impact]

    [e.g., Apple stock climbed 2.5%, hitting a 3-week high.]

    3. Stock Price Dynamics
    [If applicable, note any significant price movement trends, volatility, etc.]

    [e.g., Apple stock hit a new 52-week high post earnings beat.]
    """

    combined_content += "\n\n" + analyst_summary

    # Send the extracted content and analyst summary to OpenRouter API
    response2 = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer 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",  # Replace with your actual API key
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1-zero:free",
            "messages": [
                {
                    "role": "user",
                    "content": combined_content  # Send the extracted content along with the analyst summary
                }
            ],
        })
    )

    # Check if the request was successful
    if response2.status_code == 200:
        result2 = response2.json()
        
        # Extract and print the model's response
        daily_summary2 = result2["choices"][0]["message"]["content"]
        print(f"DeepSeek response for {stock_ticker} (Daily Summary):", daily_summary2)

unique_stocks = df["Ticker"].unique()

for stock_ticker in unique_stocks:
    print(f"Extracting articles for {stock_ticker}...")

    df_filtered = df[df["Ticker"].str.upper() == stock_ticker.upper()]

    articles_content = []
    for index, row in df_filtered.iterrows():
        url = row["Link"]
        result = extract_article_content(url)
        
        if result:
            article_text = f"Title: {result['title']}\nAuthors: {', '.join(result['authors']) if result['authors'] else 'Unknown'}\nDate: {result['date'] if result['date'] else 'Unknown'}\n\n{result['text']}\nEOF"
            articles_content.append(article_text)

    combined_content = "\n\n".join(articles_content)

    print(f"Length of combined content for {stock_ticker}: {len(combined_content)}")
    print(f"First 500 characters of combined content:\n{combined_content[:100]}")  # Print first 500 characters for inspection

    analyst_summary = """
    Mimic the role of an experienced financial
    analyst and distill the company's generic daily news and generate a concise daily news
    summary.
    Please structure the output exactly using the format provided below. 
    Keep the language analytical, concise, and factual. Do not add extra commentary or headings.
    
    📅 Date: [DD MMM YYYY]
    🏢 Company: [Company Name] ([Ticker Symbol])
    1. Key Company Announcements
    [Summarize any important announcements that are not stock-specific: new partnerships, leadership changes, global expansion, etc.]

    [e.g., Apple partners with DuckDuckGo to improve privacy features.]

    2. Strategic Developments
    [Include information on new business strategies, innovations, product launches, etc.]

    [e.g., Apple announces entry into the streaming industry with new series.]

    3. Corporate Sentiment
    [Provide general sentiment around the company’s recent actions (e.g., public reactions, media coverage, analyst opinions)]

    [e.g., Analysts bullish on Apple's long-term services growth.]
    """

    combined_content += "\n\n" + analyst_summary

    # Send the extracted content and analyst summary to OpenRouter API
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer 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",  # Replace with your actual API key
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1-zero:free",
            "messages": [
                {
                    "role": "user",
                    "content": combined_content  # Send the extracted content along with the analyst summary
                }
            ],
        })
    )

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        
        # Extract and print the model's response
        daily_summary = result["choices"][0]["message"]["content"]
        print(f"DeepSeek response for {stock_ticker} (Daily Summary):", daily_summary)

        # Fetch progressive summary from MongoDB if exists
        progressive_news_doc = collection.find_one({"stock": stock_ticker})
        progressive_summary = ""
        
        if progressive_news_doc:
            progressive_summary = progressive_news_doc.get('progressive_summary', "")

        # Send to OpenRouter API to generate an updated progressive summary
        updated_prompt = f"""
        Previous Progressive News: {progressive_summary}
        Daily Stock related Summary: {daily_summary}
        Daily Company Summary : {daily_summary2}
        Mimic the role of a financial analyst with the task of synthesizing an updated summary.
        Integrate the most pertinent information, distinguishing factual news and analysts' opinions.
        Please structure the output exactly using the format provided below. 
        Keep the language analytical, concise, and factual. Do not add extra commentary or headings.

        📆 Summary Period: [Start Date - End Date]
        🏢 Company: [Company Name] ([Ticker Symbol])
        1. Ongoing Trends & Recap of Previous News
        [Revisit major trends from prior summaries that remain relevant to the company's progression.]

        [e.g., Apple's focus on increasing its services division continues to be a key theme.]

        2. Stock-Specific Developments (from Daily Stock Summary)
        [Summarize the latest stock-specific news that impacts its market perception.]

        [e.g., Apple stock outperforms market after strong earnings, continuing upward trend.]

        3. General Company Progress (from Daily Company Summary)
        [Summarize any company-wide news that shapes its long-term prospects.]

        [e.g., Apple expands into streaming with original content, enhancing its services business.]

        4. Market & Analyst Sentiment Overview
        [Capture general sentiment of analysts and market trends, based on both stock and company summaries.]

        [e.g., Analysts remain bullish on Apple's future growth despite challenges in hardware sales.]

        5. Impact on Investment Considerations
        [Optional: Highlight potential implications for stock recommendations or future investment outlook.]

        [e.g., Despite sales slowdowns, Apple's strong services and new ventures position it for growth.]
        """

        response_progressive = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",  # Replace with your actual API key
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1-zero:free",
                "messages": [
                    {
                        "role": "user",
                        "content": updated_prompt
                    }
                ],
            })
        )

        if response_progressive.status_code == 200:
            progressive_result = response_progressive.json()
            progressive_summary = progressive_result["choices"][0]["message"]["content"]
            print(f"Progressive Summary for {stock_ticker}: {progressive_summary}")
            
            # Update MongoDB with the new progressive summary and daily summary
            collection.update_one(
                {"stock": stock_ticker},
                {
                    "$set": {
                        "daily_NSE_summary": daily_summary,
                        "daily_company_summary" : daily_summary2,
                        "progressive_summary": progressive_summary
                    }
                },
                upsert=True
            )
        else:
            print(f"Error generating progressive summary for {stock_ticker}: {response_progressive.status_code}")
    else:
        print(f"Error generating daily summary for {stock_ticker}: {response.status_code}")

