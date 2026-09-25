import zlib
import os

bundle_path = r"C:\Users\oldga\.gemini\antigravity-ide\brain\ba94c348-943c-471c-a99f-190ed79432c3\scratch\test_output.bundle"
target_crc = 0x4e121d11

with open(bundle_path, "rb") as f:
    data = f.read()

print(f"Data size: {len(data)}")

# 1. Standard zlib CRC32
print(f"zlib.crc32(data): {zlib.crc32(data):08x}")

# 2. CRC32 starting from header end (UnityFS header has flags, version, sizes)
# In UnityFS: header is usually 0x20 or 0x30 or after the header
for offset in [16, 20, 32, 48, 64, 128]:
    c = zlib.crc32(data[offset:])
    if c == target_crc:
        print(f"MATCH at offset {offset}!")

# 3. What if CRC check is disabled when CRC is 0?
print("Target CRC from log was: 4e121d11")
