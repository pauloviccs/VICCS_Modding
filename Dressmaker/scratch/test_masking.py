import re
import urllib.request
import urllib.parse
import json

def protect_and_translate(text):
    # Regex para tags <...> e chaves {...}
    pattern = re.compile(r'(<[^>]+>|\{[^}]+\})')
    tags = []
    
    def repl(m):
        idx = len(tags)
        tags.append(m.group(0))
        return f" XTAG{idx}X "
    
    masked = pattern.sub(repl, text)
    
    # Traduz o texto mascarado
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=pt&dt=t&q=" + urllib.parse.quote(masked)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        translated = "".join([part[0] for part in data[0] if part[0]])
    
    # Restaura as tags
    for i, tag in enumerate(tags):
        # Substitui possíveis variações com espaços ou minúsculas
        regex_token = re.compile(rf'\s*XTAG{i}X\s*', re.IGNORECASE)
        # Se for tag que não deve ter espaço colado, preservamos contextualmente
        translated = regex_token.sub(tag, translated)
    
    return translated

sample = "Use only: {0:list:{}|, } and keep <style=c1>bust</style> aligned with {1}."
print("Original:", sample)
print("Traduzido:", protect_and_translate(sample))
