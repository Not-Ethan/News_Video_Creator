from fetcher import fetch_articles, NewsArticle
from script_creator import get_summary

articles: list[NewsArticle] = fetch_articles(toFile="data.json",category='science')

print(get_summary(articles[0]))
