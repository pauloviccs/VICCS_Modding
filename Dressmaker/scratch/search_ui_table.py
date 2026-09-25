import UnityPy

backup_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\_OriginalBackup\localization-string-tables-english(en)_assets_all.bundle"
env = UnityPy.load(backup_bundle)

for obj in env.objects:
    if obj.type.name == "MonoBehaviour":
        raw = obj.read_typetree()
        if isinstance(raw, dict) and "m_TableData" in raw:
            # Check if this table has 'Play'
            items = raw["m_TableData"]
            found = []
            for it in items:
                loc = it.get("m_Localized", "")
                if any(w in loc for w in ["Play", "Options", "Discord", "Exit", "Save", "Slot", "Pause"]):
                    found.append((it.get("m_Id"), loc))
            if found:
                print(f"Table with {len(items)} items has matches:")
                for fid, loc in found[:10]:
                    print(f"  ID {fid}: {loc}")
