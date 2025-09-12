import user_input
import user_database
import fetch_news
import generate_html_code
import send_emails
from src.user_database import get_subscribers_tickers


def get_user_data():
    user_data = user_input.user_input()
    tickers_separated = user_input.separate_tickers(user_data[1])
    return user_data[0], tickers_separated

def add_user_db(email, tickers):
    user_database.add_subscribers(email, tickers)

def fetch_news_to_send(email):
    news_to_send = []
   # print(get_subscribers_tickers(email))
    data = user_database.get_subscribers_tickers(email)
    list_tickers = data[1:][:-1].split(',')
    for ticker in list_tickers:
        ticker = ticker.strip('"').strip("'")
        news_to_send.append(fetch_news.json_parser(fetch_news.fetch_news_by_ticker(ticker, 2), ticker))
    return news_to_send


def main():
    email, tickers = get_user_data()

    add_user_db(email, tickers)
    html_code = generate_html_code.generate_newsletter_html(fetch_news_to_send(email))
    send_emails.send_email(email, "Today's Stock Spam", html_code)

if __name__ == '__main__':
    main()




