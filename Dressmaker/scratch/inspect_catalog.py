import os
import struct

cat_path = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\catalog.bin"

with open(cat_path, "rb") as f:
    data = f.read()

print(f"Catalog size: {len(data)} bytes")
print("Header/first 64 bytes:", data[:64])

# Check for CRC in catalog: e05e239e in hex
# In integer: 0xe05e239e or bytes
crc_bytes_le = struct.pack("<I", 0xe05e239e)
crc_bytes_be = struct.pack(">I", 0xe05e239e)
print(f"Looking for LE: {crc_bytes_le.hex()} or BE: {crc_bytes_be.hex()}")
pos_le = data.find(crc_bytes_le)
pos_be = data.find(crc_bytes_be)
print(f"Pos LE: {pos_le}, Pos BE: {pos_be}")

# Search for the bundle name in catalog.bin
bundle_name = b"localization-string-tables-english(en)_assets_all.bundle"
pos_name = data.find(bundle_name)
print(f"Pos bundle name: {pos_name}")
if pos_name != -1:
    print(f"Around bundle name: {data[max(0, pos_name-30):pos_name+len(bundle_name)+30]}")
