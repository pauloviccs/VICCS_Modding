import UnityPy

shared_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\localization-assets-shared_assets_all.bundle"
env_shared = UnityPy.load(shared_bundle)

ui_shared_entries = {}
for obj in env_shared.objects:
    if obj.type.name == "MonoBehaviour":
        raw = obj.read_typetree()
        if isinstance(raw, dict) and raw.get("m_TableCollectionName") == "UI":
            for entry in raw.get("m_Entries", []):
                ui_shared_entries[entry.get("m_Key")] = entry.get("m_Id")

print("Keys in UI Shared Data:")
for k in ["Play", "OptionsMenu", "DiscordApp", "Exit", "PauseMenu", "SelectSaveSlot"]:
    print(f"  {k} -> ID {ui_shared_entries.get(k)}")

# Now check in backup bundle and current bundle
backup_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\_OriginalBackup\localization-string-tables-english(en)_assets_all.bundle"
curr_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\localization-string-tables-english(en)_assets_all.bundle"

def check_string_table(bundle_path, label):
    env = UnityPy.load(bundle_path)
    for obj in env.objects:
        if obj.type.name == "MonoBehaviour":
            raw = obj.read_typetree()
            if isinstance(raw, dict) and len(raw.get("m_TableData", [])) == 208:
                print(f"[{label}] Found UI string table with 208 items:")
                id_map = {it.get("m_Id"): it.get("m_Localized") for it in raw.get("m_TableData", [])}
                for k in ["Play", "OptionsMenu", "DiscordApp", "Exit", "PauseMenu", "SelectSaveSlot"]:
                    target_id = ui_shared_entries.get(k)
                    val = id_map.get(target_id)
                    print(f"  {k} (target_id {target_id}): '{val}'")

check_string_table(backup_bundle, "BACKUP")
check_string_table(curr_bundle, "CURRENT")
