import urllib.request
import urllib.parse
import json
import re

def translate_with_tags(text):
    # Regex to find tags like {0}, <style=c1>, </style>, <i>, </i>, <color=#...>, </color>
    # We can test if google translate preserves them
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=pt&dt=t&q=" + urllib.parse.quote(text)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return "".join([part[0] for part in data[0] if part[0]])

sample1 = "I saw your advertisement in the <i>Town Herald</i> last week."
sample2 = "<size=60%>Heaven help me, I'm going to have to wear this in front of other people.</size>"
sample3 = "Move the tape to measure the <style=c1>bust</style>, <style=c1>waist</style>, and <style=c1>hips</style>."
sample4 = "Use only: {0:list:{}|, }"

for s in [sample1, sample2, sample3, sample4]:
    print("Orig: ", s)
    print("Trans:", translate_with_tags(s))
    print()
