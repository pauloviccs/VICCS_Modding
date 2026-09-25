import urllib.request
import urllib.parse
import json

def translate_batch_gtx(texts):
    if not texts:
        return []
    # Junta com separador seguro
    separator = "\n----\n"
    payload = separator.join(texts)
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=pt&dt=t&q=" + urllib.parse.quote(payload)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        full_res = "".join([part[0] for part in data[0] if part[0]])
    
    parts = full_res.split("----")
    # Limpa espaços e confere contagem
    res = [p.strip() for p in parts]
    return res

test_batch = [
    "Square Bodice",
    "No Collar",
    "Cap Sleeve",
    "Bias Cut Skirt",
    "Rose needs a dress for work.",
    "Librarian Workwear",
    "Casual",
    "Cool",
    "Cute",
    "Daywear"
]

print(f"Enviando lote de {len(test_batch)} itens...")
out = translate_batch_gtx(test_batch)
print(f"Retornou {len(out)} itens:")
for orig, trans in zip(test_batch, out):
    print(f"  {orig} -> {trans}")
