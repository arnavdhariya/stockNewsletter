
def user_input():
    email = input("Enter your email: ")
    tickers = input("Enter your tickers (separated by comma): ")
    return email, tickers

def separate_tickers(tickers):
    tickers_separated = []
    for ticker in tickers.split(","):
        tickers_separated.append(ticker.strip().upper())
    return tickers_separated