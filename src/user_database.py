import sqlite3

def create_db():
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS subscribers (
                    email TEXT PRIMARY KEY,
                    tickers TEXT
                )''')
    conn.commit()
    conn.close()

def add_subscribers(email, tickers):
    create_db()
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('INSERT INTO subscribers VALUES (?, ?)', (email, tickers))
    conn.commit()
    conn.close()



