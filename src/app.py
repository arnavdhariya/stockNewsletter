# app.py
import streamlit as st
import re

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
            
            st.success("🎉 Subscription successful!")
            st.info(f"📊 You will receive updates for {len(collected_tickers)} stock(s) at {len(collected_emails)} email address(es)")
            
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
