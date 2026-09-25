dll_path = r"C:\Games\Dressmaker\Dressmaker_Data\Managed\Unity.Localization.dll"
with open(dll_path, "rb") as f:
    data = f.read()

pos = 255212
length = data[pos-1] # in #US stream or metadata
print("Raw around pos:")
print(data[pos:pos+150])
print("Decoded:")
print(data[pos:pos+150].decode('utf-16le', errors='ignore'))
