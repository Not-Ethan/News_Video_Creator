'''
Provide processed versions of top trending news articless
'''

from newsapi import NewsApiClient
from newspaper import Article
from dotenv import load_dotenv
import os
import json
from typing import TypedDict, Literal

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


def fetch_articles(category:Literal['business','entertainment','general','health','science','sports','technology'] | None=None,toFile=None) -> list[NewsArticle]:
    raw_response = news_client.get_top_headlines(country='us', category=category)
    top_headlines = raw_response['articles']
    num_responses = raw_response['totalResults']

    articles_with_content = []

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
            print(e.with_traceback())
            continue

        articles_with_content.append(json_article)

    if toFile:
        with open(toFile, "w") as outfile:
            outfile.write(json.dumps(articles_with_content, indent=4))
    return articles_with_content
