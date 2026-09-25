import UnityPy
import glob

for sa in glob.glob(r"C:\Games\Dressmaker\Dressmaker_Data\sharedassets*.assets"):
    env = UnityPy.load(sa)
    for obj in env.objects:
        if obj.type.name == "MonoBehaviour":
            try:
                raw = obj.read_typetree()
                if isinstance(raw, dict) and "m_CharacterTable" in raw:
                    chars = [c.get('m_Unicode') for c in raw.get('m_CharacterTable', [])]
                    has_a_tilde = 227 in chars
                    has_c_cedilla = 231 in chars
                    has_e_acute = 233 in chars
                    print(f"Font Asset: '{raw.get('m_Name')}' in {os.path.basename(sa)}")
                    print(f"  Total Chars: {len(chars)}, 'ã': {has_a_tilde}, 'ç': {has_c_cedilla}, 'é': {has_e_acute}")
            except:
                pass
