import UnityPy

shared_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\localization-assets-shared_assets_all.bundle"
env = UnityPy.load(shared_bundle)

print("Objects in shared_bundle:")
for obj in env.objects:
    if obj.type.name == "MonoBehaviour":
        raw = obj.read_typetree()
        if isinstance(raw, dict):
            name = raw.get("m_Name", "unnamed")
            print(f"MonoBehaviour name={name}")
            for k in raw.keys():
                if k not in ["m_GameObject", "m_Enabled", "m_Script"]:
                    v = raw[k]
                    val_str = str(v)[:60]
                    print(f"  {k} = {val_str}")
