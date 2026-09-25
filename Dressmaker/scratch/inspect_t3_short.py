import json

with open("data/raw_strings_en.json", "r", encoding="utf-8") as f:
    d = json.load(f)

t3 = d["tables"][3]["entries"]
print("Tabela 3 - entradas únicas curtas:")
short_t3 = sorted(list(set(e["text"] for e in t3 if len(e["text"]) < 40)))
print(f"Total de termos curtos em T3: {len(short_t3)}")
for s in short_t3[:50]:
    print(" ", s)
