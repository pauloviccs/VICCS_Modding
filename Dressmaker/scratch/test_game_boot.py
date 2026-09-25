import os
import shutil
import subprocess
import time
import json
import re
import struct

game_dir = r"C:\Games\Dressmaker"
aa_dir = os.path.join(game_dir, "Dressmaker_Data", "StreamingAssets", "aa")
catalog_path = os.path.join(aa_dir, "catalog.bin")
backup_catalog = os.path.join(aa_dir, "catalog.bin.bak")
bundle_path = os.path.join(aa_dir, "StandaloneWindows64", "localization-string-tables-english(en)_assets_all.bundle")
backup_bundle = os.path.join(aa_dir, "StandaloneWindows64", "_OriginalBackup", "localization-string-tables-english(en)_assets_all.bundle")

# 1. Garante backups
if not os.path.exists(backup_catalog):
    shutil.copy2(catalog_path, backup_catalog)

# 2. Carrega traduções e aplica no bundle
import UnityPy
with open("data/translations_ptbr.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

print(f"Carregando {backup_bundle}...")
env = UnityPy.load(backup_bundle)
patched_count = 0
for obj in env.objects:
    if obj.type.name == "MonoBehaviour":
        raw = obj.read_typetree()
        if isinstance(raw, dict) and "m_TableData" in raw:
            table_modified = False
            for item in raw["m_TableData"]:
                item_id = str(item.get("m_Id"))
                if item_id in translations:
                    if item.get("m_Localized") != translations[item_id]:
                        item["m_Localized"] = translations[item_id]
                        patched_count += 1
                        table_modified = True
            if table_modified:
                obj.save_typetree(raw)

print(f"Gravando bundle traduzido com {patched_count} strings...")
with open(bundle_path, "wb") as f:
    f.write(env.file.save())

# 3. Zera CRC no catalog.bin
with open(backup_catalog, "rb") as f:
    cat_bytes = bytearray(f.read())

bundle_name = "localization-string-tables-english(en)_assets_all.bundle"
pos = cat_bytes.find(bundle_name.encode('latin-1'))
sub = cat_bytes[pos:pos+200]
hex_m = re.search(rb'[0-9a-f]{32}', sub)
hash_pos = pos + hex_m.start()
crc_offset = hash_pos + 32 + 8
cat_bytes[crc_offset:crc_offset+4] = b"\x00\x00\x00\x00"

print(f"Gravando catalog.bin com CRC zerado no offset {crc_offset}...")
with open(catalog_path, "wb") as f:
    f.write(cat_bytes)

# 4. Inicia o jogo por 5 segundos
print("Iniciando Dressmaker.exe para teste...")
proc = subprocess.Popen([os.path.join(game_dir, "Dressmaker.exe")], cwd=game_dir)
time.sleep(5)
proc.terminate()
time.sleep(1)

# 5. Lê Player.log
log_path = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\Cozy Lives\Dressmaker\Player.log")
if os.path.exists(log_path):
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        log_lines = f.readlines()
    print("\n=== Linhas Relevantes de Player.log ===")
    for line in log_lines:
        if any(w in line for w in ["CRC", "AssetBundle", "Localization", "Exception", "Error", "Failed", "Dressmaker", "Play", "Menu"]):
            print("LOG:", line.strip())
