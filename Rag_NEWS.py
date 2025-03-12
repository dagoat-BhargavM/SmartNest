from googlesearch import search
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class StockNewsFetcher:
    def __init__(self):
        self.crawler = self.WebCrawler()
        
    class WebCrawler:
        def fetch_article_content(self, url):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, headers=headers, timeout=15)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract the page title and the first few paragraphs
                title = soup.title.string if soup.title else "No title"
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text().strip() for p in paragraphs[:5]])
                
                return {
                    'url': url,
                    'title': title,
                    'content': content
                }
            except Exception as e:
                logger.error(f"Error fetching content from {url}: {str(e)}")
                return None

    def get_news_articles(self, stock_name):
        try:
            # Refine the search query for news articles
            search_query = f"{stock_name} stock news site:moneycontrol.com OR site:livemint.com OR site:reuters.com OR site:thehindu.com"
            logger.info(f"Searching for: {search_query}")
            
            # Perform web search
            search_results = list(search(search_query, num_results=10))
            articles = []
            
            for url in search_results:
                if data := self.crawler.fetch_article_content(url):
                    articles.append(data)
            
            if not articles:
                return {"error": "No news articles found for the given stock."}
            
            return {"articles": articles}
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            return {"error": "Unable to fetch news articles. Please try again later."}

def format_response(output):
    if 'error' in output:
        return f"⚠️ {output['error']}\n"
    
    response = "📰 Top News Articles:\n"
    for idx, article in enumerate(output['articles'], start=1):
        response += f"{idx}. {article['title']}\n   URL: {article['url']}\n   Excerpt: {article['content'][:200]}...\n\n"
    return response.strip()

if __name__ == '__main__':
    stock_name = input("Enter the stock name to get news for: ").strip()
    fetcher = StockNewsFetcher()
    result = fetcher.get_news_articles(stock_name)
    print(format_response(result))
