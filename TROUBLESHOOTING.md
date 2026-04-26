# Troubleshooting Guide 🔧

## Common Issues & Solutions

### 1. Bot Not Starting ❌

**Error:** `ModuleNotFoundError: No module named 'telegram'`

**Solutions:**
```bash
# Solution 1: Install dependencies
pip install -r requirements.txt

# Solution 2: Update pip
pip install --upgrade pip

# Solution 3: Install specific version
pip install python-telegram-bot==20.7
```

**Error:** `Cannot find Python`

**Solutions:**
```bash
# Check Python is installed
python --version

# If not installed, download from python.org
# OR use: python3 instead of python
```

---

### 2. API Key Issues 🔑

**Error:** "API key not valid" or "API key is invalid"

**Causes & Solutions:**
1. **Wrong key copied**
   - Go to https://aistudio.google.com/app/apikey
   - Copy entire key (no spaces)
   - Paste carefully into ca_bot.py

2. **Extra spaces in key**
   - Remove spaces before/after the key
   - Use Ctrl+H (Find & Replace) to remove spaces

3. **Expired key**
   - Regenerate key from https://aistudio.google.com/app/apikey
   - Delete old key, create new one

4. **API quota exceeded**
   - Wait a few hours or start new project
   - Gemini has free tier limits

**Test your key:**
```python
# Add this to test:
import urllib.request
import json

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_KEY"
# Try generating a simple question
```

---

### 3. Telegram Token Issues 🤖

**Error:** "bot token was not supplied" or "Invalid token format"

**Solutions:**
1. **Token not copied**
   - Go back to BotFather
   - Send `/mybots`
   - Select your bot
   - Send `/token`
   - Copy the new token

2. **Token format wrong**
   - Should be: `123456789:ABCDefGHIJKLmnopQRSTuvwxyz`
   - Check no extra characters
   - Copy entire token with colon

3. **Bot created on wrong account**
   - Make sure you created bot on main Telegram account
   - Try `/start` from that account

---

### 4. Bot Not Responding in Telegram 📱

**Issue:** Bot doesn't respond to `/start`

**Solutions:**

1. **Check terminal**
   ```
   Is it showing "Bot is running! Press Ctrl+C to stop."?
   ```
   - If NO: Restart with `python ca_bot.py`
   - If YES: Continue below

2. **Verify telegram token**
   - Copy token from BotFather again
   - Replace in ca_bot.py
   - Restart bot

3. **Check internet connection**
   - Ping google.com
   - Restart router if needed

4. **Search bot correctly**
   - Use bot USERNAME (not name)
   - Should end with "bot"
   - Example: `ca_mock_test_bot`

5. **Restart Telegram**
   - Close Telegram completely
   - Reopen
   - Search for bot again

---

### 5. Questions Not Generating ❓

**Error:** "Error" message in Telegram or long wait time

**Solutions:**

1. **Internet issue**
   - Check connection
   - Try with 5 questions first
   - Check Telegram is online

2. **Gemini API down**
   - Try again in few minutes
   - Check https://status.ai.google.com/

3. **API quota exceeded**
   - Wait 24 hours for quota reset
   - Or create new Google project

4. **Large question count**
   - Try 5-10 questions first
   - Generating 20 questions takes longer
   - Takes 15-30 seconds normally

---

### 6. Python Installation Issues 🐍

**Error:** `Python is not installed` or `python: command not found`

**Windows:**
1. Download Python from https://python.org/downloads/
2. Run installer
3. **CHECK "Add Python to PATH"**
4. Click Install
5. Restart Command Prompt
6. Test: `python --version`

**Mac:**
```bash
# Using Homebrew
brew install python3

# Verify
python3 --version
```

**Linux:**
```bash
sudo apt-get install python3 python3-pip
python3 --version
```

---

### 7. File Permission Issues 🔐

**Error:** "Permission denied" when running

**Windows:**
- Right-click Command Prompt → Run as Administrator
- Then run bot

**Mac/Linux:**
```bash
chmod +x ca_bot.py
python ca_bot.py
```

---

### 8. Port Already in Use 🚪

**Error:** "Address already in use"

**Solution:**
```bash
# Kill process on that port
# Windows:
netstat -ano | findstr :PORT_NUMBER
taskkill /PID PROCESS_ID /F

# Mac/Linux:
lsof -ti:PORT_NUMBER | xargs kill -9
```

---

### 9. JSON Parsing Error 📄

**Error:** "JSON decode error" or "Invalid JSON"

**Causes:**
1. Corrupted user_stats.json
2. API returned invalid response

**Solutions:**
```bash
# Delete corrupted file
rm user_stats.json
# Bot will recreate it on next test
```

---

### 10. Memory/Resource Issues 💾

**Error:** "MemoryError" or bot becomes slow

**Solutions:**
```bash
# Restart bot
Ctrl+C

# Clear Python cache
rm -rf __pycache__
pip cache purge

# Run again
python ca_bot.py
```

---

## Diagnostic Steps 🔍

Follow these when something isn't working:

### Step 1: Check Terminal Output
```
Look for error messages when you run:
python ca_bot.py

Common keywords:
- "error"
- "failed"
- "invalid"
- "not found"
```

### Step 2: Verify Requirements
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check installed packages
pip list | grep telegram
pip list | grep google
```

### Step 3: Test Telegram
```
- Open Telegram
- Search for your bot username
- Send /start
- Check bot is in your contacts
```

### Step 4: Test API Key
```
Visit in browser:
https://aistudio.google.com/app/apikey
- Verify key exists
- Try creating new key
- Paste new key in bot
```

### Step 5: Restart Everything
```bash
# Kill bot
Ctrl+C

# Close Telegram completely

# Restart bot
python ca_bot.py

# Open Telegram and try again
```

---

## Getting Help 💬

If issues persist:

1. **Take screenshot** of error
2. **Note terminal output** with error details
3. **Check you have:**
   - ✅ Python 3.8+
   - ✅ All dependencies installed
   - ✅ Valid Telegram token
   - ✅ Valid Gemini API key
   - ✅ Internet connection

4. **Review:**
   - SETUP_GUIDE.md - Detailed steps
   - CREDENTIALS_GUIDE.md - Key configuration
   - README.md - Full documentation

---

## Emergency Reset 🚨

If everything stops working:

**Step 1: Stop the bot**
```bash
Ctrl+C
```

**Step 2: Clean up**
```bash
# Remove cache
rm -rf __pycache__

# Remove user stats if corrupted
rm user_stats.json
```

**Step 3: Reinstall dependencies**
```bash
pip install -r requirements.txt --force-reinstall
```

**Step 4: Verify credentials**
- Open ca_bot.py
- Check TELEGRAM_TOKEN and GEMINI_API_KEY
- Get new tokens if unsure

**Step 5: Start fresh**
```bash
python ca_bot.py
```

**Step 6: Test in Telegram**
- Send `/start`
- Should see welcome message

---

## Performance Optimization ⚡

To make bot run faster:

1. **Use smaller question counts**
   - Start with 5 questions
   - 20 questions can be slow

2. **Better internet**
   - Use wired connection if possible
   - Close other downloads

3. **Upgrade system**
   - More RAM helps
   - Faster CPU better
   - SSD faster than HDD

4. **API optimization**
   - Gemini API can be slow
   - Wait time is normal
   - API limits apply

---

## Rate Limiting 📊

**Gemini API Free Tier Limits:**
- ~100 requests per day
- Requests can fail if exceeded

**Solution:**
- Wait 24 hours for reset
- Or upgrade to paid tier
- Or create second project

---

## Logs & Debugging 🐛

**Enable verbose logging:**

Edit ca_bot.py and change:
```python
logging.basicConfig(level=logging.DEBUG)  # Instead of INFO
```

This will show more detailed information.

---

## When All Else Fails 🆘

1. **Restart computer**
2. **Reinstall Python fresh**
3. **Create new Telegram bot**
4. **Create new Gemini API key**
5. **Copy fresh ca_bot.py**
6. **Follow setup again**

---

**Still stuck?** Review the error message carefully - most errors tell you what's wrong!

**Happy Learning! 🎓**
