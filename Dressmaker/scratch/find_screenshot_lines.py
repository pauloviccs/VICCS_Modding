import json

with open("data/raw_strings_en.json", "r", encoding="utf-8") as f:
    d = json.load(f)

for table_idx, table in enumerate(d["tables"]):
    for e in table["entries"]:
        if "advertisement in the" in e["text"] or "hello! You must be the new dressmaker" in e["text"] or "certainly...a garment" in e["text"] or "wear this in front of other people" in e["text"]:
            print(f"Table {table_idx} | ID: {e['id']} -> {e['text']}")
