# Project Structure & File Guide 📁

Complete guide to all files in the CA Bot project.

## File Overview

```
CA-Bot/
├── ca_bot.py                 # ⭐ MAIN BOT FILE - Edit this with your keys
├── requirements.txt          # Python dependencies
├── README.md                 # Full documentation & features
├── QUICKSTART.md            # Get running in 3 minutes
├── SETUP_GUIDE.md           # Detailed step-by-step setup
├── CREDENTIALS_GUIDE.md     # API keys & configuration
├── FEATURES.md              # Complete features list & how to use
├── TROUBLESHOOTING.md       # Issues & solutions
├── PROJECT_FILES.md         # This file
├── qbank_sample.json        # Sample questions database
└── user_stats.json          # Auto-generated - user performance data
```

## File Descriptions

### 🤖 Main Application

**ca_bot.py** (Main Bot File)
- **What it does**: The entire Telegram bot application
- **Size**: ~650 lines
- **Key components**:
  - `generate_questions()` - AI question generation using Gemini API
  - `start()` - Welcome handler
  - `choose_subject/chapter/difficulty/type/count()` - Navigation handlers
  - `handle_answer()` - Process user answers
  - `submit_test()` - Calculate scores and save stats
  - `show_stats()` - Display performance metrics
  - `main()` - Bot initialization and polling

**🔧 MUST EDIT THIS FILE:**
- Lines 18-19: Replace TELEGRAM_TOKEN and GEMINI_API_KEY

---

### 📋 Configuration & Setup

**requirements.txt**
- **Purpose**: Python package dependencies
- **Content**: 
  - `python-telegram-bot==20.7` - Telegram bot framework
  - `google-generativeai==0.5.4` - Gemini API client
- **How to use**: 
  ```bash
  pip install -r requirements.txt
  ```

**CREDENTIALS_GUIDE.md**
- **Purpose**: Getting and configuring API keys
- **Content**:
  - Where to get Telegram token
  - Where to get Gemini API key
  - How to add them to bot
  - Security best practices
- **Best for**: First-time configuration

---

### 📚 Documentation

**README.md** (Full Documentation)
- **Purpose**: Complete project documentation
- **Content**:
  - Features overview
  - Installation steps
  - How to use the bot
  - Subjects & chapters list
  - Tips for best results
  - Troubleshooting basics
- **Length**: Comprehensive (~400 lines)
- **Best for**: Understanding full capabilities

**QUICKSTART.md** (3-Minute Setup)
- **Purpose**: Get the bot running immediately
- **Content**:
  - What you need
  - 4-step quick setup
  - Common issues quick fix
  - File structure overview
- **Length**: Brief (~150 lines)
- **Best for**: Impatient users/quick start

**SETUP_GUIDE.md** (Detailed Instructions)
- **Purpose**: Step-by-step complete setup
- **Content**:
  - Getting Telegram token with screenshots
  - Getting Gemini API key detailed
  - Python installation for all OS
  - Configuration options
  - Keeping bot running methods
- **Length**: Detailed (~300 lines)
- **Best for**: First-time users, detailed learners

**FEATURES.md** (What You Can Do)
- **Purpose**: Complete feature documentation
- **Content**:
  - 10 major features explained
  - Difficulty levels breakdown
  - Question types explained
  - How to use each feature
  - Best practices
  - FAQ section
- **Length**: Detailed (~400 lines)
- **Best for**: Understanding all capabilities

**TROUBLESHOOTING.md** (Issues & Solutions)
- **Purpose**: Solve common problems
- **Content**:
  - 10 major issues with solutions
  - Diagnostic steps
  - Emergency reset procedures
  - Performance optimization
  - Rate limiting info
- **Length**: Comprehensive (~350 lines)
- **Best for**: When something goes wrong

**PROJECT_FILES.md** (This File)
- **Purpose**: Explain all project files
- **Content**: What each file does and how to use it

---

### 💾 Data Files

**qbank_sample.json** (Sample Question Bank)
- **Purpose**: Example questions for testing
- **Content**:
  - Sample questions for all subjects
  - Mix of Easy, Medium, Hard, PYQ
  - Demonstrates question format
  - Shows metadata structure
- **Size**: ~1 KB
- **Format**: JSON
- **Used for**: Reference and testing

**user_stats.json** (User Performance Data)
- **Purpose**: Store user test history
- **Created**: Automatically after first test
- **Content**: Per user:
  - List of all tests taken
  - Date, subject, chapter, score
  - Performance by difficulty
- **Format**: JSON
- **Privacy**: Local storage only
- **Backup**: Create backup before major updates

---

## How to Navigate the Files

### 📖 If you want to:

**Get started quickly:**
1. Read `QUICKSTART.md` (2 minutes)
2. Follow 4 simple steps
3. Start testing!

**Understand everything:**
1. Read `README.md` (10 minutes)
2. Understand features in `FEATURES.md` (10 minutes)
3. Refer to other docs as needed

**Fix a problem:**
1. Check `TROUBLESHOOTING.md` first
2. Follow diagnostic steps
3. Try recommended solutions

**Configure credentials:**
1. Open `CREDENTIALS_GUIDE.md`
2. Get your tokens
3. Edit `ca_bot.py` lines 18-19

**Learn best practices:**
1. See `FEATURES.md` → Best Practices section
2. See `README.md` → Tips for Best Results
3. Practice consistently!

---

## File Dependencies

```
ca_bot.py (Main Bot)
    ├── requires → requirements.txt (packages)
    ├── uses → qbank_sample.json (optional reference)
    └── creates/updates → user_stats.json (stats database)

Documentation (for learning)
    ├── QUICKSTART.md (for quick setup)
    ├── SETUP_GUIDE.md (for detailed setup)
    ├── CREDENTIALS_GUIDE.md (for API keys)
    ├── README.md (for full info)
    ├── FEATURES.md (for features)
    ├── TROUBLESHOOTING.md (for issues)
    └── PROJECT_FILES.md (this file)
```

---

## Typical Workflow

### First Time User:
```
1. Read QUICKSTART.md or SETUP_GUIDE.md
2. Get API keys (CREDENTIALS_GUIDE.md)
3. Edit ca_bot.py with your keys
4. Install dependencies (pip install -r requirements.txt)
5. Run bot (python ca_bot.py)
6. Test in Telegram (/start)
7. Refer to FEATURES.md to learn all features
```

### Regular User:
```
1. Start bot (python ca_bot.py)
2. Use Telegram to take tests
3. Check progress with stats
4. Follow tips in FEATURES.md
```

### If Issues Occur:
```
1. Check TROUBLESHOOTING.md
2. Find your issue
3. Follow recommended solution
4. Try again
5. If still stuck, restart everything
```

---

## Customization Possibilities

**Want to modify?**

- **Change questions generation**: Edit `build_prompt()` function in `ca_bot.py`
- **Add new subjects**: Modify `SYLLABUS` dictionary in `ca_bot.py`
- **Change difficulty levels**: Modify `difficulty_keyboard()` in `ca_bot.py`
- **Add more chapters**: Extend chapter lists in `SYLLABUS`
- **Customize messages**: Edit text in handler functions

---

## Backup & Maintenance

**Important files to backup:**
1. `user_stats.json` - Contains user performance data
2. `ca_bot.py` - Your configured bot with keys

**Before updates:**
1. Backup `user_stats.json`
2. Backup `ca_bot.py`
3. Then update other files

**Cleanup:**
1. Delete `user_stats.json` to reset all users
2. Delete `__pycache__` folder safely
3. Clear Python cache if needed

---

## File Statistics

| File | Lines | Size | Purpose |
|------|-------|------|---------|
| ca_bot.py | ~650 | ~25 KB | Main application |
| README.md | ~400 | ~15 KB | Full docs |
| SETUP_GUIDE.md | ~300 | ~12 KB | Setup instructions |
| FEATURES.md | ~400 | ~15 KB | Feature guide |
| TROUBLESHOOTING.md | ~350 | ~13 KB | Issue resolution |
| QUICKSTART.md | ~150 | ~5 KB | Quick start |
| CREDENTIALS_GUIDE.md | ~200 | ~8 KB | API keys guide |
| requirements.txt | 2 | ~50 B | Dependencies |
| qbank_sample.json | ~150 | ~6 KB | Sample data |
| user_stats.json | Variable | ~1-100 KB | User data |

---

## Storage Space

**Minimum required:**
- Bot files: ~50 KB
- Python packages: ~50 MB
- User data: ~1 KB per 100 users

**Recommended:**
- Total: ~100 MB for comfortable operation

---

## Updating

**To update the bot:**

1. Download latest `ca_bot.py`
2. **KEEP your TELEGRAM_TOKEN and GEMINI_API_KEY**
3. **KEEP user_stats.json** (your user data!)
4. Update other files (.md files)
5. Restart bot

---

## File Integrity Checklist

After setup, verify you have:

- ✅ `ca_bot.py` with your tokens filled in
- ✅ `requirements.txt` in same folder
- ✅ Python packages installed
- ✅ At least one .md file for reference
- ✅ Valid Telegram token
- ✅ Valid Gemini API key
- ✅ Internet connection

---

## Advanced: File Modification Guide

**Safe to modify:**
- `README.md` - Documentation only
- All `.md` files - Documentation only
- `qbank_sample.json` - Reference only

**Use caution:**
- `ca_bot.py` - Main application
- `requirements.txt` - Package dependencies

**Never delete:**
- `user_stats.json` - Contains user progress!

**If you break something:**
1. Get fresh `ca_bot.py` from original
2. Add your tokens back
3. Keep `user_stats.json`
4. Restart

---

## Getting More Files

**Need additional files?**
- All files are provided in the CA-Bot folder
- Additional samples in `qbank_sample.json`
- Can add custom questions if needed

**Want to share your bot?**
- Share bot username (not token!)
- Share documentation files
- Keep tokens private

---

## Summary

**Remember:**
- 🔴 `ca_bot.py` = Your bot application (EDIT WITH YOUR KEYS)
- 📚 `.md` files = Documentation (READ FOR HELP)
- 📊 `user_stats.json` = User data (KEEP SAFE)
- 📦 `requirements.txt` = Dependencies (INSTALL ONCE)
- 📝 `qbank_sample.json` = Sample data (REFERENCE)

**Happy Learning! 🎓**
