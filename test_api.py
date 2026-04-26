import urllib.request, json
key = "AIzaSyDFr2G6olPUNXcLky8NwJJ6SMQar1CjuAk"
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}'
payload = json.dumps({'contents':[{'parts':[{'text':'Say hello in 3 words'}]}]}).encode()
req = urllib.request.Request(url, data=payload, headers={'Content-Type':'application/json'}, method='POST')
try:
    resp = urllib.request.urlopen(req)
    print("SUCCESS:", json.loads(resp.read().decode('utf-8'))['candidates'][0]['content']['parts'][0]['text'])
except Exception as e:
    print("FAILED:", e)
