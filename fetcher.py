from newsapi import NewsApiClient
from newspaper import Article
from dotenv import load_dotenv
import os
import json

load_dotenv()

news_client = NewsApiClient(os.getenv('NEWS_API_KEY'))

raw_response = news_client.get_top_headlines(country='us', category='technology')
top_headlines = raw_response['articles']
num_responses = raw_response['totalResults']

articles_with_content = []

print(top_headlines)

for article in top_headlines:
    scraped_article = Article(article['url'])
    try:
        scraped_article.download()
        scraped_article.parse()
        scraped_article.nlp()
        json_article = {'title': article['title'],'authors': article['author'], 'url': article['url'], 'published_at': article['publishedAt'], 'content': scraped_article.text, 'keywords': scraped_article.keywords, 'summary': scraped_article.summary, 'source': article['source']}
    except Exception as e:
        print(e)
        continue

    articles_with_content.append(json_article)



with open("data.json", "w") as outfile:
    outfile.write(json.dumps(articles_with_content, indent=4))