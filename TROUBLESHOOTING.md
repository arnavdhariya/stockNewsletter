# Email Troubleshooting Guide

## Common Issues and Solutions

### 1. ❌ "Email credentials not found in environment variables"

**Problem**: Your `.env` file is missing or not properly configured.

**Solution**:
1. Create a `.env` file in the root directory (`stockNewsletter/`)
2. Add these lines:
   ```
   EMAIL=your_email@gmail.com
   PASSWORD=your_app_password
   NEWS_API_KEY=your_news_api_key
   ```
3. Make sure there are no spaces around the `=` sign
4. Don't use quotes around the values

### 2. ❌ "Authentication failed"

**Problem**: Gmail authentication is failing.

**Solutions**:
1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and generate a password
   - Use this 16-character password in your `.env` file (NOT your regular Gmail password)

### 3. ❌ "Recipient email rejected"

**Problem**: The email address is invalid or blocked.

**Solutions**:
1. Check the email address is correct
2. Try sending to a different email address
3. Make sure the recipient email accepts emails from your Gmail account

### 4. ❌ "Server disconnected"

**Problem**: Network or Gmail server issues.

**Solutions**:
1. Check your internet connection
2. Try again in a few minutes
3. Make sure Gmail SMTP is not blocked by your firewall

## Step-by-Step Testing

### Step 1: Check Environment Variables
1. Open the Admin Panel in your Streamlit app
2. Look for the "Environment Check" section
3. Make sure all three items show ✅ green checkmarks

### Step 2: Send a Simple Test Email
1. In the Admin Panel, find "Send Test Email"
2. Enter your own email address
3. Click "Send Simple Test Email"
4. Watch the detailed logs to see where it fails

### Step 3: Check Your Inbox
1. Check your inbox (and spam folder)
2. If you don't receive the email, the issue is with Gmail authentication
3. If you receive it, the issue might be with the newsletter content

## Gmail App Password Setup (Detailed)

1. **Go to Google Account**: https://myaccount.google.com/
2. **Security tab** → **2-Step Verification**
3. **Turn on 2-Step Verification** if not already enabled
4. **App passwords** → **Select app** → **Mail**
5. **Select device** → **Other (custom name)** → Enter "Stock Newsletter"
6. **Generate** → Copy the 16-character password
7. **Add to .env file**: `PASSWORD=your_16_character_app_password`

## Testing Checklist

- [ ] `.env` file exists in root directory
- [ ] `.env` file contains EMAIL, PASSWORD, and NEWS_API_KEY
- [ ] Gmail has 2-Factor Authentication enabled
- [ ] Using App Password (not regular password)
- [ ] App Password is 16 characters long
- [ ] No spaces around `=` in `.env` file
- [ ] Test email address is valid
- [ ] Internet connection is working
- [ ] Check spam folder for test emails

## Still Not Working?

If you're still having issues:

1. **Check the Streamlit logs** for detailed error messages
2. **Try a different email provider** (like Outlook) to test if it's Gmail-specific
3. **Verify your Gmail account** isn't locked or restricted
4. **Contact support** with the specific error message from the logs
