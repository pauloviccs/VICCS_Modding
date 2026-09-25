import json

with open("data/raw_strings_en.json", "r", encoding="utf-8") as f:
    d = json.load(f)

all_strings = {}
for table in d["tables"]:
    for e in table["entries"]:
        all_strings[str(e["id"])] = e["text"]

print(f"Total de IDs: {len(all_strings)}")
unique_texts = set(all_strings.values())
print(f"Total de Textos Únicos: {len(unique_texts)}")

# Agrupa por tamanho de texto
short_texts = [t for t in unique_texts if len(t) <= 30]
medium_texts = [t for t in unique_texts if 30 < len(t) <= 120]
long_texts = [t for t in unique_texts if len(t) > 120]

print(f"Textos curtos (<=30 chars - tags, peças, botões): {len(short_texts)}")
print(f"Textos médios (31-120 chars - falas, descrições): {len(medium_texts)}")
print(f"Textos longos (>120 chars - artigos, cartas): {len(long_texts)}")
