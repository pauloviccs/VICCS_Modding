import os

dll_path = r"C:\Games\Dressmaker\Dressmaker_Data\Managed\Unity.Addressables.dll"
with open(dll_path, "rb") as f:
    dll_data = f.read()

# Let's search for "CRC Mismatch"
# Remember the log message:
# "CRC Mismatch. Provided e05e239e, calculated 4e121d11 from data. Will not load AssetBundle 'aa\StandaloneWindows64\localization-string-tables-english(en)_assets_all.bundle'"
# That message was printed by Unity!
# Where was that message printed? Not in Unity.Localization.dll.
# Let's check which DLL or native engine printed "CRC Mismatch"!
search_crc_msg = b"CRC Mismatch"
managed_dir = r"C:\Games\Dressmaker\Dressmaker_Data\Managed"
import glob
for dll in glob.glob(os.path.join(managed_dir, "*.dll")):
    try:
        with open(dll, "rb") as f:
            c = f.read()
            if search_crc_msg in c or b"CRC Mismatch" in c:
                print(f"Found 'CRC Mismatch' in {os.path.basename(dll)}")
    except:
        pass
