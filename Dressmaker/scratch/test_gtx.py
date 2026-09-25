import urllib.request
import urllib.parse
import json

def translate_gt(text, src='en', dest='pt'):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={src}&tl={dest}&dt=t&q=" + urllib.parse.quote(text)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return "".join([part[0] for part in data[0] if part[0]])
    except Exception as e:
        return None

print("Teste 1:", translate_gt("Oh—oh, hello! You must be the new dressmaker?"))
print("Teste 2:", translate_gt("Square Bodice"))
print("Teste 3:", translate_gt("Rose needs a dress for work."))
print("Teste 4:", translate_gt("Librarian Workwear"))
