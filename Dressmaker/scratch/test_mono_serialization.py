import UnityPy

backup_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\_OriginalBackup\localization-string-tables-english(en)_assets_all.bundle"
env = UnityPy.load(backup_bundle)

# Lets find the MonoBehaviour for UI_en (count=208)
for obj in env.objects:
    if obj.type.name == "MonoBehaviour":
        raw = obj.read_typetree()
        if isinstance(raw, dict) and len(raw.get("m_TableData", [])) == 208:
            orig_raw_data = obj.get_raw_data()
            print(f"Original raw bytes length: {len(orig_raw_data)}")
            
            # Now let's save typetree WITHOUT CHANGING ANYTHING
            obj.save_typetree(raw)
            new_raw_data = obj.get_raw_data()
            print(f"New raw bytes length (no changes): {len(new_raw_data)}")
            print(f"Bytes identical: {orig_raw_data == new_raw_data}")
            if orig_raw_data != new_raw_data:
                print("Divergence found! Finding first difference...")
                for i in range(min(len(orig_raw_data), len(new_raw_data))):
                    if orig_raw_data[i] != new_raw_data[i]:
                        print(f"Diff at byte {i}: orig={orig_raw_data[i]:02x} ({orig_raw_data[i:i+16]}), new={new_raw_data[i]:02x} ({new_raw_data[i:i+16]})")
                        break
