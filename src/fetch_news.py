import json
import os
import urllib

from dotenv import load_dotenv
import datetime
import requests
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news_by_ticker(ticker, max_results=2):
    date = datetime.date.today()
    query = urllib.parse.quote(ticker)
    # "https://newsapi.org/v2/everything?q=AAPL%20Inc&sortBy=publishedAt&language=en&pageSize=5&apiKey=9d828964fa4242a3aa599a90aa69b3df"

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&sortBy=publishedAt&"
        f"language=en&pageSize={max_results}&apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    return response.json()


def json_parser(data, ticker):
    parsed = []
    for article in data["articles"]:
        curr_entry = {}
        curr_entry["ticker"] = ticker
        curr_entry["name"] = article["source"]["name"]
        curr_entry["author"] = article["author"]
        curr_entry["title"] = article["title"]
        curr_entry["description"] = article["description"]
        curr_entry["url"] = article["url"]
        curr_entry["image"] = article["urlToImage"]
        parsed.append(curr_entry)
    return parsed

if __name__ == "__main__":
    print(json_parser(fetch_news_by_ticker("AAPL")))


