import json

with open("data/raw_strings_en.json", "r", encoding="utf-8") as f:
    d = json.load(f)

t1 = d["tables"][1]["entries"]
print("Tabela 1 - total de falas:", len(t1))
# Let's inspect Rose's dialogues specifically
rose_dialogues = [e for e in t1 if "dressmaker" in e["text"].lower() or "rose" in e["text"].lower() or "work" in e["text"].lower()]
print(f"Falas contendo termos-chave: {len(rose_dialogues)}")
for e in rose_dialogues[:15]:
    print(f"  [{e['id']}] {e['text']}")
