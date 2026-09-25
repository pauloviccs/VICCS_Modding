import os
import glob

managed_dir = r"C:\Games\Dressmaker\Dressmaker_Data\Managed"
search_utf16 = "No translation found".encode("utf-16le")

for dll in glob.glob(os.path.join(managed_dir, "*.dll")):
    try:
        with open(dll, "rb") as f:
            content = f.read()
            if search_utf16 in content:
                print(f"Found UTF-16 in {os.path.basename(dll)}")
    except Exception:
        pass
