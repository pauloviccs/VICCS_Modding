import UnityPy

bundle_path = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\localization-assets-english(en)_assets_all.bundle"
env = UnityPy.load(bundle_path)

for obj in env.objects:
    print(f"Type: {obj.type.name}, Name: {getattr(obj, 'name', 'N/A')}")
    if obj.type.name == "MonoBehaviour":
        raw = obj.read_typetree()
        if isinstance(raw, dict) and "m_Name" in raw:
            print(f"  MonoBehaviour Name: {raw['m_Name']}")
            if "m_CharacterTable" in raw:
                chars = [c.get('m_Unicode') for c in raw.get('m_CharacterTable', [])]
                has_a_tilde = 227 in chars
                has_c_cedilla = 231 in chars
                has_e_acute = 233 in chars
                print(f"  TextMeshPro Font Asset: {raw['m_Name']}")
                print(f"  Chars: {len(chars)}, 'ã': {has_a_tilde}, 'ç': {has_c_cedilla}, 'é': {has_e_acute}")
