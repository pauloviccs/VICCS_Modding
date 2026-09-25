import os

dll_path = r"C:\Games\Dressmaker\Dressmaker_Data\Managed\Unity.Addressables.dll"
with open(dll_path, "rb") as f:
    data = f.read()

# Check for crc in Addressables
import re
print("Searching for Crc in Unity.Addressables.dll:")
matches = re.findall(rb'[A-Za-z0-9_]{3,30}Crc[A-Za-z0-9_]{0,30}', data)
for m in set(matches):
    print(" ", m.decode('latin-1'))
