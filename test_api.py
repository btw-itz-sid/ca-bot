import urllib.request, json
url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=AIzaSyB-pBZKqk-H6c-y6PxDgkYG3ZOaM2Ur1Fs'
payload = json.dumps({'contents':[{'parts':[{'text':'Say hello'}]}]}).encode()
req = urllib.request.Request(url, data=payload, headers={'Content-Type':'application/json'}, method='POST')
try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode('utf-8'))
    print("SUCCESS:", data['candidates'][0]['content']['parts'][0]['text'])
except Exception as e:
    print("FAILED:", e)
