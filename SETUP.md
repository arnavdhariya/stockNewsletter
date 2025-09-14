# Stock Newsletter Setup Guide

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Gmail account** with App Password enabled
3. **News API key** from https://newsapi.org/

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd stockNewsletter
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file:**
   Create a `.env` file in the root directory with:
   ```
   EMAIL=your_email@gmail.com
   PASSWORD=your_app_password
   NEWS_API_KEY=your_news_api_key
   ```

## Gmail Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
   - Use this password in your `.env` file

## News API Setup

1. Go to https://newsapi.org/
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file

## Running the Application

1. **Start the Streamlit app:**
   ```bash
   streamlit run src/app.py
   ```

2. **Open your browser** to the URL shown in the terminal (usually http://localhost:8501)

## Features

- **Subscription Form**: Users can enter emails and stock tickers
- **Daily Emails**: Automatically sends newsletters at 10:00 AM daily
- **Admin Panel**: Send test emails and view subscribers
- **Database Storage**: SQLite database stores subscriber information
- **News Integration**: Fetches latest news for subscribed tickers

## File Structure

```
stockNewsletter/
├── src/
│   ├── app.py              # Main Streamlit application
│   ├── fetch_news.py       # News API integration
│   ├── generate_html_code.py # Email template generation
│   ├── send_emails.py      # Email sending functionality
│   ├── user_database.py    # Database operations
│   └── subscribers.db      # SQLite database (created automatically)
├── requirements.txt        # Python dependencies
└── .env                   # Environment variables (create this)
```

## Troubleshooting

- **Email not sending**: Check your Gmail App Password and 2FA settings
- **News not fetching**: Verify your News API key is correct
- **Database errors**: Ensure the `src/` directory is writable
- **Scheduler not working**: The app must be running continuously for daily emails

## Notes

- The application runs a background scheduler for daily emails
- Keep the Streamlit app running for the scheduler to work
- For production, consider using a proper server or cloud service
