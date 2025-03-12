import ssl
import re
import time
import nltk
import pandas as pd
from newspaper import Article
from nltk.tokenize import sent_tokenize
import requests
import json

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)  

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

csv_file_path = 'complete_stocks_news.csv'
df = pd.read_csv(csv_file_path)

unique_stocks = df["Stock"].unique()

for stock_ticker in unique_stocks:
    print(f"Extracting articles for {stock_ticker}...")

    df_filtered = df[df["Stock"].str.upper() == stock_ticker.upper()]

    articles_content = []
    for index, row in df_filtered.iterrows():
        url = row["News Article Link"]
        result = extract_article_content(url)
        
        if result:
            article_text = f"Title: {result['title']}\nAuthors: {', '.join(result['authors']) if result['authors'] else 'Unknown'}\nDate: {result['date'] if result['date'] else 'Unknown'}\n\n{result['text']}\nEOF"
            articles_content.append(article_text)

    combined_content = "\n\n".join(articles_content)

    print(f"Length of combined content for {stock_ticker}: {len(combined_content)}")
    print(f"First 500 characters of combined content:\n{combined_content[:500]}")  # Print first 500 characters for inspection

    analyst_summary = """
    Mimic the role of an experienced financial
    analyst with the task of synthesizing an updated and detailed summary by considering all articles 
    provided above and let the summary be of good length.
    Instructions: Integrate the most pertinent information,
    distinguish factual news and analysts' opinions.
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
        output = result["choices"][0]["message"]["content"]
        print(f"DeepSeek response for {stock_ticker}:", output)
    else:
        print(f"Error for {stock_ticker}: {response.status_code}, {response.text}")
