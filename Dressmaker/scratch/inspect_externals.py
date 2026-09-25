import UnityPy

original_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\localization-string-tables-english(en)_assets_all.bundle"
backup_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\_OriginalBackup\localization-string-tables-english(en)_assets_all.bundle"

orig_env = UnityPy.load(backup_bundle)
curr_env = UnityPy.load(original_bundle)

orig_sf = list(orig_env.files.values())[0]
curr_sf = list(curr_env.files.values())[0]

print(f"Orig SerializedFile: {type(orig_sf)}")
print(f"Curr SerializedFile: {type(curr_sf)}")

if hasattr(orig_sf, "externals"):
    print(f"Orig externals: {orig_sf.externals}")
if hasattr(curr_sf, "externals"):
    print(f"Curr externals: {curr_sf.externals}")

if hasattr(orig_sf, "m_externals"):
    print(f"Orig m_externals: {orig_sf.m_externals}")
if hasattr(curr_sf, "m_externals"):
    print(f"Curr m_externals: {curr_sf.m_externals}")

for k in dir(orig_sf):
    if "ext" in k.lower():
        print(f"found attr: {k} = {getattr(orig_sf, k)}")
        print(f"curr attr: {k} = {getattr(curr_sf, k)}")
