import re
import struct

cat_path = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\catalog.bin"
with open(cat_path, "rb") as f:
    cat_data = f.read()

# Find all .bundle mentions
for m in re.finditer(rb'[\w\(\)\-\.]+\.bundle', cat_data):
    bname = m.group(0).decode('latin-1')
    start = m.start()
    end = m.end()
    # Let's inspect next 100 bytes after bundle name
    after = cat_data[end:end+150]
    # Search for non-zero 4-byte ints
    print(f"\nBundle: {bname} at offset {start}")
    # Search for known hashes
    # Look at the 32-char hex string right after
    hex_m = re.search(rb'[0-9a-f]{32}', after)
    if hex_m:
        hex_offset = end + hex_m.start()
        after_hex = cat_data[hex_offset+32:hex_offset+64]
        # In after_hex, the CRC is at offset 8 (after two 32-bit ints)
        ints = struct.unpack("<IIII", after_hex[:16])
        print(f"  Hex hash: {hex_m.group(0).decode('latin-1')}")
        print(f"  Ints after hash: {ints[0]:x}, {ints[1]:x}, CRC={ints[2]:x} (offset {hex_offset+32+8}), {ints[3]:x}")
