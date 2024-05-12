from newsapi import NewsApiClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

news_client = NewsApiClient(os.getenv('NEWS_API_KEY'))

raw_response = news_client.get_top_headlines(country='us', category='technology')
top_headlines = raw_response['articles']
num_responses = raw_response['totalResults']

with open("data.json", "w") as outfile:
    outfile.write(json.dumps(top_headlines, indent=4))