'''
Provide processed versions of top trending news articless
'''

from newsapi import NewsApiClient
from newspaper import Article
from dotenv import load_dotenv
import os
import json
from typing import TypedDict, Literal, Callable
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

news_client = NewsApiClient(os.getenv('NEWS_API_KEY'))

class Source(TypedDict):
    name: str
    id: str
class NewsArticle(TypedDict):
    title: str
    author: list[str]
    url: str
    published_at: str
    content: str
    keywords: list[str]
    source: Source


def fetch_articles(category:Literal['business','entertainment','general','health','science','sports','technology'] | None=None,to_file=None) -> list[NewsArticle]:
    raw_response = news_client.get_top_headlines(country='us', category=category)
    top_headlines = raw_response['articles']

    #add content to top headlines - news client truncates to 200 lines
    articles_with_content:list[NewsArticle] = []
    for article in top_headlines:
        scraped_article = Article(article['url'])
        try:
            scraped_article.download()
            scraped_article.parse()
            scraped_article.nlp()
            json_article: NewsArticle = {
                'title': article['title'],
                'author': article['author'], 
                'url': article['url'], 
                'published_at': article['publishedAt'], 
                'content': scraped_article.text, 
                'keywords': scraped_article.keywords, 
                'source': article['source']
                }
        except Exception as e:
            logging.exception("Error fetching")
            continue

        articles_with_content.append(json_article)
    
    #sometimes article is empty
    filter_conditions: Callable[[NewsArticle], bool] = lambda article: article.get("content") != "" or article.get("title").lower()=="[removed]"
    filtered_articles = list(filter(filter_conditions, articles_with_content))

    if to_file:
        with open(to_file, "w") as outfile:
            outfile.write(json.dumps(filtered_articles, indent=4))
    return filtered_articles
