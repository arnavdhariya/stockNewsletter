import sqlite3
import json

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
    c.execute('INSERT INTO subscribers VALUES (?, ?)', (email, str(tickers)))
    conn.commit()
    conn.close()

def get_subscribers_tickers(email):
    create_db()
    conn = sqlite3.connect('subscribers.db')
    c = conn.cursor()
    c.execute('SELECT tickers FROM subscribers WHERE email = ?', (email,))
    rows = c.fetchall()
    return rows[0][0]



