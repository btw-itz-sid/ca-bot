"""
Quick test to verify your Gemini API key works.
Run: python test_api.py
"""
import os
import sys
import urllib.request
import urllib.error
import json
import time
from dotenv import load_dotenv

# Fix Windows console encoding for emojis
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY is not set in .env file!")
    exit(1)

print(f"Testing API key: {GEMINI_API_KEY[:10]}...")

# Test 1: List models (checks if key is valid)
print("\n--- Test 1: Checking API key validity ---")
try:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    print(f"✅ API key is VALID! Found {len(data.get('models', []))} models")
except urllib.error.HTTPError as e:
    if e.code == 403:
        print("❌ API key is INVALID/REVOKED (403 Forbidden)")
        print("   Fix: Go to https://aistudio.google.com/apikey and create a NEW key")
    elif e.code == 429:
        print("⚠️ Rate limited on model listing (429) — key is probably valid, just overloaded")
    else:
        print(f"❌ HTTP Error {e.code}")
    exit(1)

# Test 2: Generate a simple question (with retry for 429)
print("\n--- Test 2: Generating a test question ---")
models = ["gemini-2.0-flash", "gemini-2.5-flash-lite"]
success = False

for model in models:
    for attempt in range(3):
        try:
            print(f"  Trying {model} (attempt {attempt + 1})...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            payload = json.dumps({
                "contents": [{"parts": [{"text": "Generate 1 MCQ about accounting. Return ONLY JSON: [{\"q\":\"question\",\"opts\":[\"A\",\"B\",\"C\",\"D\"],\"ans\":0}]"}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1024}
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            print(f"✅ Question generated successfully with {model}!")
            print(f"   Response: {text[:200]}...")
            success = True
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = [5, 15, 30][attempt]
                print(f"  ⚠️ Rate limited (429), waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  ❌ HTTP {e.code} on {model}, trying next model...")
                break
        except Exception as e:
            print(f"  ❌ Error: {e}")
            break
    if success:
        break

if success:
    print("\n🎉 All tests passed! Your bot will work fine.")
    print("   Deploy to Railway: git add -A && git commit -m 'fix' && git push")
else:
    print("\n❌ Could not generate questions. Wait 1-2 minutes and try again.")
    print("   Free tier has 15 requests/minute limit.")
