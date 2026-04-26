import urllib.request, json, re

GEMINI_API_KEY = "AIzaSyDU2inIdY_vYxVETAhtRNj3PbEPGS0qHp4"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

prompt = """Generate exactly 2 MCQ questions about Indian Contract Act 1872 - Offer and Acceptance for CA Foundation June 2026.
Return ONLY a raw JSON array:
[{"q":"Question?","type":"mcq","opts":["A) opt1","B) opt2","C) opt3","D) opt4"],"ans":0,"exp":"explanation"}]"""

payload = json.dumps({
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
}).encode("utf-8")

req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")

try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode("utf-8"))
    raw = data["candidates"][0]["content"]["parts"][0]["text"]
    clean = re.sub(r"```json|```", "", raw).strip()
    match = re.search(r"\[.*\]", clean, re.DOTALL)
    if match:
        clean = match.group(0)
    questions = json.loads(clean)
    print(f"SUCCESS! Generated {len(questions)} questions\n")
    for i, q in enumerate(questions):
        print(f"Q{i+1}: {q['q']}")
        for opt in q['opts']:
            print(f"  {opt}")
        print(f"  Answer: {q['opts'][q['ans']]}")
        print(f"  Explanation: {q['exp']}\n")
except Exception as e:
    print(f"FAILED: {e}")
