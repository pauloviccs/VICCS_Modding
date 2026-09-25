import UnityPy
import os

env = UnityPy.load(r"C:\Games\Dressmaker\Dressmaker_Data\resources.assets")
for obj in env.objects:
    if obj.type.name == "MonoBehaviour":
        try:
            raw = obj.read_typetree()
            if isinstance(raw, dict) and "m_GlyphTable" in raw:
                name = raw.get("m_Name", "unnamed")
                print(f"Font Asset em resources.assets: {name}")
                # In TMP, m_CharacterTable maps unicode to glyph index!
                chars = [c.get('m_Unicode') for c in raw.get('m_CharacterTable', [])]
                has_a_tilde = 227 in chars
                has_c_cedilla = 231 in chars
                has_e_acute = 233 in chars
                print(f"  Total characters: {len(chars)}")
                print(f"  Suporta 'ã': {has_a_tilde}, 'ç': {has_c_cedilla}, 'é': {has_e_acute}")
        except:
            pass
