import UnityPy

backup_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\_OriginalBackup\localization-string-tables-english(en)_assets_all.bundle"
orig_env = UnityPy.load(backup_bundle)
orig_bf = list(orig_env.files.values())[0]
sf = list(orig_bf.files.values())[0]

print("SerializedFile attrs:")
for a in dir(sf):
    if not a.startswith("__"):
        val = getattr(sf, a)
        if not callable(val):
            print(f"  {a} = {val}")
