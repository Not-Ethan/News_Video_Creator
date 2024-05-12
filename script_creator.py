from transformers import pipeline
from fetcher import NewsArticle
pipe = pipeline("text2text-generation", model="AndreLiu1225/t5-news-summarizer")

def get_summary(article: NewsArticle):
    return pipe(article.get('content'))