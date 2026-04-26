# CA Bot Setup Guide 🎓

This guide will help you set up and run the CA Foundation Mock Test Bot in a few simple steps.

## Step 1: Get Your Telegram Bot Token 🤖

### How to Create a Telegram Bot:

1. **Open Telegram App** on your phone or go to [web.telegram.org](https://web.telegram.org)

2. **Search for BotFather**
   - Search "@BotFather" in Telegram's search bar

3. **Start the conversation**
   - Click on BotFather
   - Send `/newbot` command

4. **Answer the questions**
   - Question: "Alright, a new bot. How are we going to call it?"
   - Answer: Type your bot name (e.g., "CA Mock Test Bot")
   - Question: "Good. Now let's choose a username for your bot"
   - Answer: Type a username (e.g., "ca_mock_test_bot", must end with "bot")

5. **Get your token**
   - BotFather will send you a message with:
   ```
   Done! Congratulations on your new bot. You'll find it at 
   t.me/your_bot_name. You can now add a description, about 
   section and profile picture for your bot, see /help for a 
   list of commands.
   
   Use this token to access the HTTP API:
   1234567890:ABCdefGHIJKlmNOPqrsTUVwxYZ1a2b3c4d5e
   ```
   - **Copy the token** (the long string at the end)

## Step 2: Get Your Google Gemini API Key 🔑

### How to Create a Gemini API Key (Free!):

1. **Go to Google AI Studio**
   - Visit [https://aistudio.google.com](https://aistudio.google.com)

2. **Sign in with your Google account**
   - If you don't have one, create a free Google account

3. **Click "Get API Key"**
   - In the left sidebar, find "Get API Key"
   - Or go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

4. **Create API Key**
   - Click "Create API key in new project"
   - Or "Create API key"

5. **Copy your API Key**
   - You'll see your API key
   - Click the copy button next to it
   - **Save this key somewhere safe**

## Step 3: Install Python 3.8+ 🐍

### Windows:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important:** Check "Add Python to PATH" during installation
4. Click Install

### Mac:
```bash
# Using Homebrew
brew install python3
```

### Linux:
```bash
sudo apt-get install python3 python3-pip
```

## Step 4: Download and Configure the Bot 📥

### Option A: Using Command Line (Recommended)

1. **Open Terminal/Command Prompt**
   - Windows: Press `Win + R`, type `cmd`, press Enter
   - Mac: Press `Cmd + Space`, type `terminal`, press Enter
   - Linux: Open your terminal app

2. **Navigate to your folder**
   ```bash
   cd Desktop/CA-Bot
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Edit ca_bot.py with your credentials**
   
   Open `ca_bot.py` in a text editor (Notepad, VS Code, etc.)
   
   Find these lines (around line 18-19):
   ```python
   TELEGRAM_TOKEN = "8575203310:AAGwDKwdbaEVc_ckvV0rMH2lbwek65LUC9U"
   GEMINI_API_KEY = "AIzaSyDGUxchTah_ql52RC7dO8_rMyAwoB-dteE"
   ```
   
   Replace with your actual tokens:
   ```python
   TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN_HERE"
   GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
   ```
   
   **Example:**
   ```python
   TELEGRAM_TOKEN = "1234567890:ABCdefGHIJKlmNOPqrsTUVwxYZ1a2b3c4d5e"
   GEMINI_API_KEY = "AIzaSyDGUxchTah_ql52RC7dO8_rMyAwoB-dteE"
   ```

## Step 5: Run Your Bot 🚀

In your terminal, type:

```bash
python ca_bot.py
```

You should see:
```
Bot is running! Press Ctrl+C to stop.
```

**Success!** Your bot is now live! 🎉

## Step 6: Test Your Bot 🧪

1. **Open Telegram**
2. **Search for your bot** (using the username you created)
3. **Send `/start`**
4. You should see a welcome message
5. Start taking mock tests!

## Common Issues & Solutions 🔧

### Issue: "ModuleNotFoundError: No module named 'telegram'"
**Solution:**
```bash
pip install --upgrade python-telegram-bot
```

### Issue: "API key not valid" error
**Solution:**
1. Check your Gemini API key is copied correctly
2. Make sure there are no extra spaces before/after
3. Regenerate the key from aistudio.google.com

### Issue: Bot not responding in Telegram
**Solution:**
1. Check terminal - is bot still running?
2. Verify Telegram token is correct
3. Restart the bot (Ctrl+C, then run again)

### Issue: "Connection refused" error
**Solution:**
1. Check internet connection
2. Try restarting the bot
3. Check if firewall is blocking connections

## Tips for Using the Bot 💡

### First Time Users:
1. Start with **Easy** difficulty
2. Choose **5 questions** to get familiar
3. Read explanations carefully
4. Progress to **Medium** level

### For Regular Practice:
1. Mix difficulty levels
2. Try **PYQ (Previous Year Questions)**
3. Take tests **2-3 times per week**
4. Review your **stats regularly**

### Maximize Learning:
1. Don't rush through questions
2. Try to solve before revealing answer
3. Understand explanations
4. Retake chapters you score low on

## Keeping the Bot Running 🔄

### Option 1: Run on Your Computer
- Keep the terminal open
- Computer must stay on
- Simple for personal use

### Option 2: Use a VPS (Advanced)
- For continuous access
- Use services like:
  - AWS EC2 (Free tier available)
  - Google Cloud
  - Heroku
  - DigitalOcean
  - PythonAnywhere

## Next Steps 📚

1. **Customize the bot** (optional):
   - Add more chapters
   - Modify difficulty levels
   - Add new subjects

2. **Share with friends**:
   - Share your bot username
   - They can start using it!

3. **Track progress**:
   - Stats are saved automatically
   - Check your progress regularly
   - Aim for improvement!

## Need Help? 🆘

If you encounter issues:
1. Check this guide carefully
2. Verify all API keys are correct
3. Ensure Python 3.8+ is installed
4. Try restarting the bot
5. Check internet connection

## File Structure 📁

After setup, your folder should look like:
```
CA-Bot/
├── ca_bot.py              # Main bot file (EDIT THIS with your keys)
├── requirements.txt        # Dependencies
├── README.md              # General information
├── SETUP_GUIDE.md         # This file
└── user_stats.json        # Created automatically on first test
```

## Security Tips 🔒

1. **Never share your API keys** with anyone
2. **Keep tokens private** - don't post them online
3. **Don't commit keys to GitHub** - if using version control
4. **Regenerate keys** if you accidentally exposed them

## Start Now! 🎯

You're all set! Follow the 6 steps above and you'll have your CA mock test bot running in minutes!

```
Happy Learning! All the Best! 💪
```
