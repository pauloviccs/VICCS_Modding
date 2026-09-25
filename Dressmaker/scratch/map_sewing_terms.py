import json
import re

with open("data/raw_strings_en.json", "r", encoding="utf-8") as f:
    d = json.load(f)

t3 = d["tables"][3]["entries"]
tags = []
for e in t3:
    txt = e["text"]
    if any(k in txt for k in ["Collar", "Sleeve", "Bodice", "Skirt", "Trim", "Button", "Brooch", "Belt", "Fabric"]):
        tags.append(txt)

print(f"Total de itens com termos de costura em T3: {len(tags)}")
for t in sorted(list(set(tags)))[:40]:
    print(" ", t)
