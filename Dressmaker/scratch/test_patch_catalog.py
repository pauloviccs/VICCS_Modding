import os
import re
import struct

def find_bundle_crc_offset(catalog_bytes, bundle_name):
    pos = catalog_bytes.find(bundle_name.encode('latin-1'))
    if pos == -1:
        return None
    # Procurar hash hex de 32 chars após o nome do bundle
    sub = catalog_bytes[pos:pos+200]
    hex_m = re.search(rb'[0-9a-f]{32}', sub)
    if not hex_m:
        return None
    hash_pos = pos + hex_m.start()
    crc_offset = hash_pos + 32 + 8
    crc_val = struct.unpack("<I", catalog_bytes[crc_offset:crc_offset+4])[0]
    return crc_offset, crc_val

catalog_path = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\catalog.bin"
with open(catalog_path, "rb") as f:
    data = bytearray(f.read())

bundle_name = "localization-string-tables-english(en)_assets_all.bundle"
res = find_bundle_crc_offset(data, bundle_name)
print(f"Resultado da busca dinâmica: {res}")
if res:
    offset, old_crc = res
    print(f"CRC antigo no offset {offset}: 0x{old_crc:08x} ({old_crc})")
    # Zera o CRC
    data[offset:offset+4] = b"\x00\x00\x00\x00"
    new_crc = struct.unpack("<I", data[offset:offset+4])[0]
    print(f"Novo CRC no offset {offset}: 0x{new_crc:08x} ({new_crc})")
