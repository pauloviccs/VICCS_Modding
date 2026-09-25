import re
import urllib.request
import urllib.parse
import json

def protect_braces_and_translate(text):
    # Regex apenas para chaves {0}, {1}, {0:list...}
    pattern = re.compile(r'\{[^}]+\}')
    tags = []
    
    def repl(m):
        idx = len(tags)
        tags.append(m.group(0))
        return f"__T{idx}__"
    
    masked = pattern.sub(repl, text)
    
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=pt&dt=t&q=" + urllib.parse.quote(masked)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        translated = "".join([part[0] for part in data[0] if part[0]])
    
    for i, tag in enumerate(tags):
        token = f"__T{i}__"
        translated = re.sub(rf'\s*{re.escape(token)}\s*', f" {tag} ", translated)
        translated = translated.replace(f"  {tag}", f" {tag}").replace(f"{tag}  ", f"{tag} ")
    
    return translated.strip()

sample1 = "Move the tape to measure the <style=c1>bust</style>, <style=c1>waist</style>, and <style=c1>hips</style>."
sample2 = "Use only: {0:list:{}|, } and avoid {1}."
sample3 = "I saw your advertisement in the <i>Town Herald</i> last week."

for s in [sample1, sample2, sample3]:
    print("Orig: ", s)
    print("Trans:", protect_braces_and_translate(s))
    print()
