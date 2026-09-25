import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.backend.patcher import ModPatcher

patcher = ModPatcher(r"C:\Games\Dressmaker")
print("Status inicial do patcher:", patcher.get_status())

with open("data/translations_ptbr.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

print(f"Total de traduções no arquivo: {len(translations)}")

print("\n--- Aplicando Tradução Completa (5886 Strings) ---")
manifest = patcher.apply_patch(translations, progress_callback=lambda p, msg: print(f"[{p}%] {msg}"))
print("Manifesto pós-instalação:", manifest)
print("Status final do patcher:", patcher.get_status())
