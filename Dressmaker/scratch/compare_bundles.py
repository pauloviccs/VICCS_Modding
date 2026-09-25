import os
import UnityPy

original_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\localization-string-tables-english(en)_assets_all.bundle"
backup_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\_OriginalBackup\localization-string-tables-english(en)_assets_all.bundle"

if not os.path.exists(backup_bundle):
    print("Backup não existe ainda!")
    exit(0)

orig_env = UnityPy.load(backup_bundle)
curr_env = UnityPy.load(original_bundle)

print(f"Original bundle objects: {len(orig_env.objects)}")
print(f"Current bundle objects: {len(curr_env.objects)}")

for i, (orig_obj, curr_obj) in enumerate(zip(orig_env.objects, curr_env.objects)):
    print(f"Obj {i}: orig type={orig_obj.type.name}, curr type={curr_obj.type.name}")
    if orig_obj.type.name == "MonoBehaviour":
        t_orig = orig_obj.read_typetree()
        t_curr = curr_obj.read_typetree()
        print(f"  Orig TableData count: {len(t_orig.get('m_TableData', [])) if isinstance(t_orig, dict) else 'N/A'}")
        print(f"  Curr TableData count: {len(t_curr.get('m_TableData', [])) if isinstance(t_curr, dict) else 'N/A'}")
        print(f"  Orig m_SharedData: {t_orig.get('m_SharedData') if isinstance(t_orig, dict) else 'N/A'}")
        print(f"  Curr m_SharedData: {t_curr.get('m_SharedData') if isinstance(t_curr, dict) else 'N/A'}")
        print(f"  Orig m_LocaleId: {t_orig.get('m_LocaleId') if isinstance(t_orig, dict) else 'N/A'}")
        print(f"  Curr m_LocaleId: {t_curr.get('m_LocaleId') if isinstance(t_curr, dict) else 'N/A'}")
