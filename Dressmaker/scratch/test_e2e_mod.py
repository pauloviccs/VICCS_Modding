import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.backend.patcher import ModPatcher

patcher = ModPatcher(r"C:\Games\Dressmaker")
print("Status inicial:", patcher.get_status())

# Carrega traduções
with open("data/translations_ptbr.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

print(f"Total de traduções a aplicar: {len(translations)}")

# 1. Aplica patch
print("\n--- Testando Instalação do Mod ---")
manifest = patcher.apply_patch(translations, progress_callback=lambda p, msg: print(f"[{p}%] {msg}"))
print("Manifesto gerado:", manifest)
print("Status após instalação:", patcher.get_status())

# 2. Testa leitura do bundle para certificar que o idioma mudou
bundle_path = patcher.get_bundle_path()
import UnityPy
env = UnityPy.load(bundle_path)
found_pt = False
for obj in env.objects:
    if obj.type.name == "MonoBehaviour":
        raw = obj.read_typetree()
        if isinstance(raw, dict) and "m_TableData" in raw:
            for item in raw["m_TableData"]:
                if item.get("m_Id") == 56515267379200: # Language -> Idioma
                    print(f"Confirmação no Bundle após patch: ID 56515267379200 = '{item['m_Localized']}'")
                    found_pt = (item['m_Localized'] == "Idioma")

assert found_pt, "Falha: O termo 'Idioma' não foi encontrado no bundle!"
print(">>> Validação de patch: SUCESSO ABSOLUTO! <<<")

# 3. Testa restauração
print("\n--- Testando Restauração / Desinstalação ---")
patcher.restore_original()
print("Status após restauração:", patcher.get_status())

# Verifica se voltou ao original
env_restored = UnityPy.load(bundle_path)
found_original = False
for obj in env_restored.objects:
    if obj.type.name == "MonoBehaviour":
        raw = obj.read_typetree()
        if isinstance(raw, dict) and "m_TableData" in raw:
            for item in raw["m_TableData"]:
                if item.get("m_Id") == 56515267379200:
                    print(f"Confirmação no Bundle após restauração: ID 56515267379200 = '{item['m_Localized']}'")
                    found_original = (item['m_Localized'] == "Language")

assert found_original, "Falha: O bundle não voltou ao original!"
print(">>> Validação de restauração: SUCESSO ABSOLUTO! <<<")
