import UnityPy

curr_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\localization-string-tables-english(en)_assets_all.bundle"
curr_env = UnityPy.load(curr_bundle)
curr_bf = list(curr_env.files.values())[0]
sf = list(curr_bf.files.values())[0]

print("Curr SerializedFile attrs:")
print("  header:", sf.header)
print("  unity_version:", sf.unity_version)
print("  version:", sf.version)
print("  ref_types:", len(sf.ref_types), sf.ref_types)
print("  externals:", sf.externals)
print("  assetbundle:", sf.assetbundle)
