import json

with open("data/raw_strings_en.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Tabela 3: Content (1930 strings)
t3 = data["tables"][3]["entries"]
print(f"Total Tabela 3: {len(t3)}")
print("Amostra Tabela 3:")
for it in t3[:25]:
    print(f"  {it['id']} -> {it['text']}")

# Tabela 1: Dialogue (3677 strings)
t1 = data["tables"][1]["entries"]
print(f"\nTotal Tabela 1: {len(t1)}")
print("Amostra Tabela 1:")
for it in t1[:25]:
    print(f"  {it['id']} -> {it['text'][:80]}...")
