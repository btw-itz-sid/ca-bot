# CA Bot - Quick Start Guide ⚡

Get your CA mock test bot running in **3 minutes**!

## What You Need 📋

1. **Telegram Account** (free)
2. **Google Account** (free)
3. **Python 3.8+** installed

## 3-Minute Setup 🚀

### Step 1: Get Your Tokens (1 minute)

**Telegram Bot Token:**
- Go to Telegram → Search "@BotFather"
- Send `/newbot`
- Follow prompts, get your token

**Gemini API Key:**
- Visit https://aistudio.google.com
- Click "Get API Key"
- Copy your free API key

### Step 2: Install Dependencies (1 minute)

Open Terminal/Command Prompt in your CA-Bot folder:

```bash
pip install -r requirements.txt
```

### Step 3: Add Your Keys (30 seconds)

Edit `ca_bot.py` and replace:
```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN_HERE"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

### Step 4: Run the Bot (30 seconds)

```bash
python ca_bot.py
```

You should see:
```
Bot is running! Press Ctrl+C to stop.
```

**Done!** 🎉

## Start Using 📱

1. Open Telegram
2. Search for your bot
3. Send `/start`
4. Begin taking mock tests!

## What's Included ✨

✅ **4 Subjects**:
- Accounts 📊
- Business Laws ⚖️  
- Maths & Stats 📐
- Economics 📈

✅ **4 Difficulty Levels**:
- 🟢 Easy
- 🟡 Medium
- 🔴 Tough
- ⭐ Previous Year Questions (PYQ)

✅ **Features**:
- AI-Generated Questions
- Multiple Question Types (MCQ, True/False)
- Progress Tracking
- Instant Scoring
- Explanations for all answers

## Tips 💡

**For Best Results:**
1. Start with Easy
2. Move to Medium (Recommended)
3. Try Tough questions last
4. Don't skip PYQ

**Take at least 2-3 tests per week** for consistent improvement!

## Folder Files 📁

- `ca_bot.py` - **Main bot (EDIT YOUR KEYS HERE)**
- `requirements.txt` - Dependencies
- `README.md` - Full documentation
- `SETUP_GUIDE.md` - Detailed setup
- `qbank_sample.json` - Sample questions
- `user_stats.json` - Created automatically

## Troubleshooting 🔧

**Bot won't start?**
- Check Python is installed: `python --version`
- Verify dependencies: `pip install -r requirements.txt`

**No questions loading?**
- Verify Gemini API key
- Check internet connection
- Try with fewer questions first

**Telegram bot not responding?**
- Check terminal is still running
- Verify Telegram token is correct
- Search for your bot by exact username

## Need More Help? 📚

- See `SETUP_GUIDE.md` for detailed instructions
- Read `README.md` for full features
- Check terminal output for error messages

## That's It! 🎓

You're ready to start practicing CA mock tests!

**Happy Learning! All the Best! 💪**

---

*Enjoy unlimited CA Foundation questions based on ICAI's 2023 Syllabus*
