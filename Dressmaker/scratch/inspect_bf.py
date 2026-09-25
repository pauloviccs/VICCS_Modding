import UnityPy

backup_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\_OriginalBackup\localization-string-tables-english(en)_assets_all.bundle"
curr_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\localization-string-tables-english(en)_assets_all.bundle"

orig_env = UnityPy.load(backup_bundle)
curr_env = UnityPy.load(curr_bundle)

orig_bf = list(orig_env.files.values())[0]
curr_bf = list(curr_env.files.values())[0]

for name, f in orig_bf.files.items():
    print(f"Orig internal file: {name}, type={type(f)}")
    if hasattr(f, "m_externals"):
        print(f"  orig m_externals ({len(f.m_externals)}):")
        for ext in f.m_externals:
            print(f"    guid={getattr(ext, 'guid', None)}, path={getattr(ext, 'path', None)}, name={getattr(ext, 'name', None)}")

for name, f in curr_bf.files.items():
    print(f"Curr internal file: {name}, type={type(f)}")
    if hasattr(f, "m_externals"):
        print(f"  curr m_externals ({len(f.m_externals)}):")
        for ext in f.m_externals:
            print(f"    guid={getattr(ext, 'guid', None)}, path={getattr(ext, 'path', None)}, name={getattr(ext, 'name', None)}")
