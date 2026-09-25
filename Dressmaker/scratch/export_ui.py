import json

with open('data/raw_strings_en.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# Table 2: Menus
with open('data/table_2_menus.txt', 'w', encoding='utf-8') as out:
    for e in d['tables'][2]['entries']:
        out.write(f"{e['id']} = {e['text']}\n")

# Table 0: Tutorials
with open('data/table_0_tutorials.txt', 'w', encoding='utf-8') as out:
    for e in d['tables'][0]['entries']:
        out.write(f"{e['id']} = {e['text']}\n")

print("Tabelas 2 e 0 exportadas para visualização.")
