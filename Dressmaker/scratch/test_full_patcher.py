import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.backend.patcher import ModPatcher

patcher = ModPatcher(r"C:\Games\Dressmaker")
print("Status inicial:", patcher.get_status())

with open("data/translations_ptbr.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

# 1. Aplica o patch
print("\n--- Testando Patcher Completo (Bundle + Catalog.bin) ---")
manifest = patcher.apply_patch(translations, progress_callback=lambda p, msg: print(f"[{p}%] {msg}"))
print("Manifesto gerado:", manifest)
print("Status após instalação:", patcher.get_status())

# 2. Verifica CRC no catalog.bin
catalog_path = patcher.get_catalog_path()
with open(catalog_path, "rb") as f:
    cat_bytes = f.read()

import re, struct
pos = cat_bytes.find(b"localization-string-tables-english(en)_assets_all.bundle")
sub = cat_bytes[pos:pos+250]
hex_m = re.search(rb'[0-9a-f]{32}', sub)
hash_pos = pos + hex_m.start()
crc_offset = hash_pos + 32 + 8
crc_val = struct.unpack("<I", cat_bytes[crc_offset:crc_offset+4])[0]
print(f"CRC no catalog.bin após patch: {crc_val} (Esperado: 0)")
assert crc_val == 0, "Falha: O CRC não foi zerado no catalog.bin!"

print(">>> Teste de Instalação e Catalog Bypass: SUCESSO ABSOLUTO! <<<")
