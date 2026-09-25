import os
import glob
import winreg

print("=== Checking AppData LocalLow ===")
appdata = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow")
for root, dirs, files in os.walk(appdata):
    if "dressmaker" in root.lower():
        print(f"Dir: {root}")
        for f in files:
            print(f"  File: {f}")

print("\n=== Checking Registry ===")
try:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Cozy Llama\Dressmaker")
    i = 0
    while True:
        try:
            name, val, typ = winreg.EnumValue(key, i)
            if "lang" in name.lower() or "locale" in name.lower() or "selected" in name.lower():
                print(f"Reg: {name} = {val}")
            i += 1
        except OSError:
            break
except Exception as e:
    print(f"Registry read error: {e}")
