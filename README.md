# CA Foundation Mock Test Bot 📚

A Telegram bot for practicing CA Foundation mock tests with AI-generated questions based on ICAI's new syllabus (2023). 

## Features ✨

✅ **Difficulty Levels**: Easy, Medium, and Tough questions  
✅ **Previous Year Questions (PYQ)**: Real exam-style questions  
✅ **4 Subjects**: Accounts, Business Laws, Maths & Stats, Economics  
✅ **Multiple Chapter Coverage**: 10+ chapters per subject  
✅ **MCQ & True/False**: Mixed question types  
✅ **AI-Powered Questions**: Using Google Gemini API  
✅ **Progress Tracking**: View your test history and average scores  
✅ **Score Analysis**: Performance metrics by difficulty level  

## Setup Instructions 🚀

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token (get from BotFather on Telegram)
- Google Gemini API Key

### Installation

1. **Clone or Download the Bot**
```bash
cd CA-Bot
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API Keys**

Open `ca_bot.py` and replace these with your actual keys:
```python
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

### Getting API Keys

**Telegram Bot Token:**
1. Open Telegram and search for `@BotFather`
2. Type `/newbot` and follow instructions
3. Copy your bot token

**Google Gemini API Key:**
1. Go to [Google AI Studio](https://aistudio.google.com)
2. Click "Get API Key" 
3. Create a new API key for free
4. Copy and use it in the bot

### Running the Bot

```bash
python ca_bot.py
```

You should see:
```
Bot is running! Press Ctrl+C to stop.
```

## How to Use 📖

### Starting the Bot
1. Open Telegram
2. Search for your bot name
3. Click `/start` to begin

### Taking a Mock Test
1. **Choose Subject**: Select from Accounts, Laws, Maths, or Economics
2. **Select Chapter**: Pick a specific chapter from the subject
3. **Choose Difficulty**: 
   - 🟢 Easy: Fundamental concepts
   - 🟡 Medium: Application-based (Recommended)
   - 🔴 Tough: Complex scenarios
   - ⭐ PYQ: Previous year exam questions
4. **Select Type**: MCQ only, True/False only, or Mixed
5. **Set Question Count**: 5, 10, 15, or 20 questions
6. **Answer Questions**: Read each question and select your answer
7. **Submit & Review**: Get instant feedback with explanations

### Navigation
- **Next/Prev**: Navigate between questions
- **Submit Test**: Finish the test and see results
- **Show Stats**: View your performance history

## Question Database 📊

The bot generates questions using **Google Gemini AI**, which ensures:
- ✅ Unique questions every time
- ✅ Realistic ICAI exam-style questions
- ✅ Difficulty-level specific content
- ✅ Comprehensive explanations

## User Stats 📈

Your performance is automatically saved in `user_stats.json`:
- Total tests completed
- Average score
- Performance by difficulty level
- Last 5 test records

## Subjects & Chapters 📚

### Accounts (📊)
- Theoretical Framework
- Accounting Process
- Bank Reconciliation
- Inventories Valuation
- Depreciation
- Special Transactions
- Sole Proprietor Final Accounts
- Partnership Accounting
- Company Accounts
- Branch Accounting

### Business Laws (⚖️)
- Indian Contract Act (4 chapters)
- Sale of Goods Act
- Partnership Act
- LLP Act
- Companies Act (2 chapters)
- Negotiable Instruments Act

### Maths & Stats (📐)
- Ratio, Proportion, Indices
- Equations
- Linear Inequalities
- Time Value of Money
- Permutations & Combinations
- Sequences & Series
- Sets, Functions, Relations
- Calculus Basics
- Statistical Description
- Central Tendency
- Dispersion Measures
- Probability
- Distributions
- Correlation & Regression
- Index Numbers

### Economics (📈)
- Business Economics Introduction
- Demand & Supply
- Production & Cost
- Market Price Determination
- Business Cycles
- National Income
- Public Finance
- Money Market
- International Trade
- Indian Economy Overview

## Tips for Best Results 💡

1. **Start with Easy**: Build confidence with easy level first
2. **Mix Difficulty**: Gradually move to medium and tough levels
3. **Review PYQ**: Previous year questions are crucial
4. **Use Explanations**: Always read explanations after each question
5. **Track Progress**: Monitor your improvement over time
6. **Consistent Practice**: Take at least 2-3 tests per week

## Troubleshooting 🔧

**Bot not responding?**
- Check internet connection
- Verify Telegram token is correct
- Ensure bot is still running

**Questions taking too long to load?**
- Gemini API might be slow
- Try again with fewer questions (5 questions first)
- Check your internet speed

**API Key errors?**
- Verify your Gemini API key is active
- Check if you have API quota remaining
- Regenerate key if needed

## File Structure 📁

```
CA-Bot/
├── ca_bot.py           # Main bot file
├── requirements.txt    # Dependencies
├── user_stats.json     # User progress (auto-generated)
└── README.md          # This file
```

## Features Coming Soon 🚀

- [ ] Offline question bank
- [ ] Performance graphs
- [ ] Timed tests
- [ ] Chapter-wise comparative analysis
- [ ] Doubt section
- [ ] Study materials links

## Support & Issues 🆘

If you encounter any issues:
1. Check the README troubleshooting section
2. Verify API keys are correct
3. Restart the bot
4. Check Python version compatibility

## License 📜

Free to use for personal education purposes.

## About ICAI 🏛️

This bot is based on the **Institute of Chartered Accountants of India (ICAI)** CA Foundation syllabus (2023). All questions are AI-generated and for practice purposes only.

---

**Happy Learning! All the best for your CA exams! 🎓**

For questions or updates, keep this bot running and enjoy unlimited practice! 💪
