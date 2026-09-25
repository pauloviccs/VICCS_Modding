import json

with open("data/raw_strings_en.json", "r", encoding="utf-8") as f:
    d = json.load(f)

tags = ["Professional", "Casual", "Cool", "Cute", "Daywear", "Eclectic", "Elaborate", "Elegant", "Eveningwear", "Flowers", "Formal", "Glamour", "Gothic", "Patterned", "Playful", "Risqué", "Romantic", "Shimmering", "Simple", "Uncomfortable", "Warm", "Workwear", "Sew", "Rotate", "Change Speed", "Reset", "No Collar", "No Sleeves", "Square Bodice", "Cap Sleeve", "Bias Cut Skirt", "Librarian Workwear"]

found = {}
for t_idx, t in enumerate(d["tables"]):
    for e in t["entries"]:
        txt = e["text"].strip()
        if txt in tags:
            found[txt] = (t_idx, e["id"])

print(f"Encontrados {len(found)} de {len(tags)} tags/termos:")
for k, v in found.items():
    print(f"  {k} -> Tabela {v[0]}, ID {v[1]}")
