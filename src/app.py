# app.py
import streamlit as st
import re
import smtplib
import schedule
import time
import threading
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import sqlite3
import requests
import urllib
import datetime

load_dotenv()

from fetch_news import fetch_news_by_ticker, json_parser
from generate_html_code import generate_newsletter_html

def create_db():
    db_path = os.path.join(os.path.dirname(__file__), 'subscribers.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS subscribers (
                    email TEXT PRIMARY KEY,
                    tickers TEXT
                )''')
    conn.commit()
    conn.close()

def add_subscriber(email, tickers):
    create_db()
    db_path = os.path.join(os.path.dirname(__file__), 'subscribers.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO subscribers VALUES (?, ?)', (email, str(tickers)))
    conn.commit()
    conn.close()

def get_all_subscribers():
    create_db()
    db_path = os.path.join(os.path.dirname(__file__), 'subscribers.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM subscribers')
    rows = c.fetchall()
    conn.close()
    return rows

# Email functions
def send_email(to_email, subject, body_html):
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body_html, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        return True
    except smtplib.SMTPAuthenticationError as e:
        return False
    except smtplib.SMTPRecipientsRefused as e:
        return False
    except smtplib.SMTPServerDisconnected as e:
        return False

def send_daily_newsletters():

    subscribers = get_all_subscribers()
    
    if not subscribers:
        return

    for email, tickers_str in subscribers:
        tickers = eval(tickers_str) if tickers_str else []
        news_data = []
        for ticker in tickers:

            news = fetch_news_by_ticker(ticker, 2)
            parsed_news = json_parser(news, ticker)
            news_data.extend(parsed_news)
            
        if not news_data:
            continue
        html_content = generate_newsletter_html(news_data)
        send_email(email, "Daily Stock Newsletter", html_content)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

schedule.every().day.at("10:00").do(send_daily_newsletters)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_ticker(ticker):
    ticker = ticker.strip().upper()
    return re.match(r'^[A-Z0-9]{1,5}$', ticker) is not None

def parse_emails(email_input):
    if not email_input:
        return []
    
    emails = [email.strip() for email in email_input.split(',')]
    valid_emails = []
    invalid_emails = []
    
    for email in emails:
        if email and validate_email(email):
            valid_emails.append(email)
        elif email:
            invalid_emails.append(email)
    
    return valid_emails, invalid_emails

def parse_tickers(ticker_input):
    if not ticker_input:
        return []
    
    tickers = [ticker.strip() for ticker in ticker_input.split(',')]
    valid_tickers = []
    invalid_tickers = []
    
    for ticker in tickers:
        if ticker and validate_ticker(ticker):
            valid_tickers.append(ticker.upper())
        elif ticker:
            invalid_tickers.append(ticker)
    
    return valid_tickers, invalid_tickers

def collect_subscription_data():
    collected_emails = []
    collected_tickers = []

    with st.form("subscription_form"):
        st.subheader("Email Address")
        email_input = st.text_input(
            "Enter your email address (or multiple emails separated by commas)",
            placeholder="example@email.com, another@email.com",
            help="You can enter multiple email addresses separated by commas"
        )
        
        st.subheader("Stock Tickers")
        ticker_input = st.text_input(
            "Enter stock tickers (separated by commas)",
            placeholder="AAPL, GOOGL, MSFT, TSLA",
            help="Enter stock symbols separated by commas (e.g., AAPL, GOOGL, MSFT)"
        )
        
        submitted = st.form_submit_button("Subscribe to Newsletter", type="primary")

    if submitted:
        valid_emails, invalid_emails = parse_emails(email_input)
        valid_tickers, invalid_tickers = parse_tickers(ticker_input)

        if valid_emails:
            st.success(f"Valid emails: {', '.join(valid_emails)}")
        
        if invalid_emails:
            st.error(f"Invalid emails: {', '.join(invalid_emails)}")
        
        if valid_tickers:
            st.success(f"Valid tickers: {', '.join(valid_tickers)}")
        
        if invalid_tickers:
            st.error(f"Invalid tickers: {', '.join(invalid_tickers)}")

        if valid_emails and valid_tickers:
            collected_emails = valid_emails
            collected_tickers = valid_tickers
            
            # Save to database
            for email in collected_emails:
                add_subscriber(email, collected_tickers)
            
            st.success("🎉 Subscription successful!")
            st.info(f"📊 You will receive updates for {len(collected_tickers)} stock(s) at {len(collected_emails)} email address(es)")
            st.info("📧 Daily newsletters will be sent at 10:00 AM")
            
            # Display summary
            with st.expander("Subscription Summary"):
                st.write("**Email Addresses:**")
                for email in collected_emails:
                    st.write(f"• {email}")
                
                st.write("**Stock Tickers:**")
                for ticker in collected_tickers:
                    st.write(f"• {ticker}")
            
            st.sidebar.subheader("📊 Collected Data")
            st.sidebar.write("**Emails:**", collected_emails)
            st.sidebar.write("**Tickers:**", collected_tickers)
            
        elif not valid_emails and not valid_tickers:
            st.warning("Please enter at least one valid email and one valid stock ticker.")
        elif not valid_emails:
            st.warning("Please enter at least one valid email address.")
        elif not valid_tickers:
            st.warning("Please enter at least one valid stock ticker.")
    
    return collected_emails, collected_tickers

st.title("Stock Spam Subscription")
st.markdown("Enter your email and stock tickers to subscribe to our newsletter!")

emails, tickers = collect_subscription_data()

if emails and tickers:
    st.markdown("---")
    st.markdown("### 📊 Collected Data")
    st.write(f"**Valid Emails:** {emails}")
    st.write(f"**Valid Tickers:** {tickers}")


st.markdown("---")
st.markdown("### Instructions")
st.markdown("""
- **Email**: Enter one or more email addresses separated by commas
- **Stock Tickers**: Enter stock symbols (1-5 characters) separated by commas
- Examples: `AAPL, GOOGL, MSFT` or `TSLA, NVDA, AMZN`
""")

with st.expander("Examples"):
    st.markdown("""
    **Email Examples:**
    - `user@example.com`
    - `user1@example.com, user2@example.com`
    
    **Ticker Examples:**
    - `AAPL` (Apple)
    - `GOOGL, MSFT, TSLA` (Google, Microsoft, Tesla)
    - `NVDA, AMZN, META` (NVIDIA, Amazon, Meta)
    """)