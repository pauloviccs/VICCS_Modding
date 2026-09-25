import json

with open("data/translations_ptbr.json", "r", encoding="utf-8") as f:
    d = json.load(f)

# IDs dos screenshots anteriores
test_ids = [
    ("Rose intro", "7392685334564988"),
    ("Rose ad", "7392685334564989"),
    ("Rose reaction", "7392685334565011"),
    ("Square Bodice", "22892765499985921"),
    ("Librarian Workwear", "1474902723903551"),
    ("No Collar", "3287807748456460"),
    ("No Sleeves", "3287807748456491"),
    ("Sew", "67952245194815"),
    ("Professional", "67952241000461"),
    ("Workwear", "67952241000467"),
    ("Play", "21752065242939392"),
    ("Options", "64301694959616"),
]

print("Validação de Amostras:")
for label, str_id in test_ids:
    print(f"  {label} ({str_id}) -> {d.get(str_id)}")
