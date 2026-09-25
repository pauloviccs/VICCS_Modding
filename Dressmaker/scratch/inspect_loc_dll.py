import os

dll_path = r"C:\Games\Dressmaker\Dressmaker_Data\Managed\Unity.Localization.dll"
with open(dll_path, "rb") as f:
    data = f.read()

target = "No translation found".encode("utf-16le")
idx = 0
while True:
    pos = data.find(target, idx)
    if pos == -1:
        break
    start = max(0, pos - 100)
    end = min(len(data), pos + 200)
    print(f"Match at {pos}:")
    snippet = data[start:end]
    # Tenta decodificar trechos legíveis
    for s in snippet.split(b"\x00\x00"):
        try:
            print("  ", s.decode("utf-16le", errors="ignore"))
        except:
            pass
    idx = pos + len(target)
