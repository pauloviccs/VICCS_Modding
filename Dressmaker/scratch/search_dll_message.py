import os
import glob

managed_dir = r"C:\Games\Dressmaker\Dressmaker_Data\Managed"
search_str = b"No translation found"

for dll in glob.glob(os.path.join(managed_dir, "*.dll")):
    try:
        with open(dll, "rb") as f:
            content = f.read()
            if search_str in content:
                print(f"Found in {os.path.basename(dll)}")
            elif b"in UI" in content:
                print(f"Found 'in UI' in {os.path.basename(dll)}")
    except Exception:
        pass
