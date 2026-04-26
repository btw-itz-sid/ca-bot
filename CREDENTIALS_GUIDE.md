# Configuration Template for CA Bot

This file shows you what credentials you need and where to get them.

## Required Credentials

### 1. TELEGRAM_TOKEN
**What it is:** Your bot's unique identifier for Telegram

**How to get it:**
1. Open Telegram
2. Search for "@BotFather"
3. Send `/newbot`
4. Choose a name for your bot (e.g., "CA Mock Test Bot")
5. Choose a username ending with "bot" (e.g., "ca_mock_test_bot")
6. BotFather will send you a token like:
   ```
   Done! Use this token to access the HTTP API:
   1234567890:ABCdefGHIJKlmNOPqrsTUVwxYZ1a2b3c4d5e
   ```
7. Copy this entire token

**Example:**
```
TELEGRAM_TOKEN = "1234567890:ABCdefGHIJKlmNOPqrsTUVwxYZ1a2b3c4d5e"
```

### 2. GEMINI_API_KEY
**What it is:** API key to access Google's Gemini AI for question generation

**How to get it:**
1. Go to https://aistudio.google.com/
2. Sign in with your Google account (create one if needed)
3. Look for "Get API Key" button on the left sidebar
4. Click "Create API Key"
5. Click "Create API key in new project"
6. Copy the API key shown

**Example:**
```
GEMINI_API_KEY = "AIzaSyDGUxchTah_ql52RC7dO8_rMyAwoB-dteE"
```

## How to Configure

### Method 1: Direct Edit (Recommended for local use)

1. Open `ca_bot.py` in any text editor
2. Find lines 18-19:
   ```python
   TELEGRAM_TOKEN = "8575203310:AAGwDKwdbaEVc_ckvV0rMH2lbwek65LUC9U"
   GEMINI_API_KEY = "AIzaSyDGUxchTah_ql52RC7dO8_rMyAwoB-dteE"
   ```
3. Replace with your actual credentials:
   ```python
   TELEGRAM_TOKEN = "YOUR_ACTUAL_TOKEN_HERE"
   GEMINI_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
   ```
4. Save the file

### Method 2: Using Environment Variables (Recommended for production)

If you want to use environment variables instead:

**Windows (Command Prompt):**
```
set TELEGRAM_TOKEN=your_token_here
set GEMINI_API_KEY=your_api_key_here
```

**Mac/Linux (Terminal):**
```
export TELEGRAM_TOKEN=your_token_here
export GEMINI_API_KEY=your_api_key_here
```

Then modify `ca_bot.py` to read from environment:
```python
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

## Security Best Practices

⚠️ **IMPORTANT:** Never share your tokens/keys publicly!

1. **Don't commit to GitHub** - If using version control, add credentials to `.gitignore`
2. **Don't share in messages** - Your tokens give access to your bot/API quota
3. **Keep safe** - Store in a secure location
4. **Regenerate if exposed** - If accidentally shared, regenerate immediately:
   - Telegram: Use BotFather `/revoke` command
   - Gemini: Delete key from https://aistudio.google.com/app/apikey

## Verification

After adding credentials, test if they work:

1. Run the bot:
   ```
   python ca_bot.py
   ```

2. You should see:
   ```
   Bot is running! Press Ctrl+C to stop.
   ```

3. Open Telegram and search for your bot
4. Send `/start` - you should get a welcome message
5. If no errors appear in terminal, you're good!

## Troubleshooting

**Error: "bot token was not supplied"**
- Your TELEGRAM_TOKEN is empty or incorrect
- Verify token is copied completely
- Check no extra spaces

**Error: "API key not valid"**
- Your GEMINI_API_KEY is incorrect
- Verify it's copied from https://aistudio.google.com/app/apikey
- Check for extra spaces

**Error: "Connection refused"**
- Internet connection issue
- Check firewall settings
- Restart your router

## File to Edit

**Location:** `ca_bot.py` (lines 18-19)

**Content to find:**
```python
TELEGRAM_TOKEN = "8575203310:AAGwDKwdbaEVc_ckvV0rMH2lbwek65LUC9U"
GEMINI_API_KEY = "AIzaSyDGUxchTah_ql52RC7dO8_rMyAwoB-dteE"
```

**Replace with your keys** - that's it!

## Questions?

Refer to the appropriate guide:
- `QUICKSTART.md` - Get running in 3 minutes
- `SETUP_GUIDE.md` - Detailed step-by-step
- `README.md` - Full documentation

**Happy Learning! 🎓**
