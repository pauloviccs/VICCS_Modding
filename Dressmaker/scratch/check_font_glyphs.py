import UnityPy
import os
import glob

# Procurar onde estão os SDF fonts do TextMeshPro
sharedassets = glob.glob(r"C:\Games\Dressmaker\Dressmaker_Data\*.assets")
for sa in sharedassets:
    env = UnityPy.load(sa)
    for obj in env.objects:
        if "Font" in obj.type.name or obj.type.name == "MonoBehaviour":
            try:
                raw = obj.read_typetree()
                if isinstance(raw, dict) and "m_GlyphTable" in raw:
                    print(f"Font Asset encontrado em {os.path.basename(sa)}: {raw.get('m_Name')}")
                    # Check unicode range in glyphs
                    unicodes = [g.get('m_Index') for g in raw.get('m_GlyphTable', [])]
                    # Check for 'ã' (0x00E3 = 227), 'ç' (0x00E7 = 231), 'é' (0x00E9 = 233)
                    has_a_tilde = any(g.get('m_Index') == 227 for g in raw.get('m_GlyphTable', []))
                    has_c_cedilla = any(g.get('m_Index') == 231 for g in raw.get('m_GlyphTable', []))
                    has_e_acute = any(g.get('m_Index') == 233 for g in raw.get('m_GlyphTable', []))
                    print(f"  Total glyphs: {len(raw.get('m_GlyphTable', []))}")
                    print(f"  Suporta 'ã': {has_a_tilde}, 'ç': {has_c_cedilla}, 'é': {has_e_acute}")
            except:
                pass
