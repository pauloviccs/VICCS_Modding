import zlib
import struct

# Let's test the backup bundle CRC vs expected 0xe05e239e
backup_bundle = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\_OriginalBackup\localization-string-tables-english(en)_assets_all.bundle"

with open(backup_bundle, "rb") as f:
    orig_data = f.read()

crc_orig = zlib.crc32(orig_data)
print(f"Original bundle zlib.crc32: {crc_orig:08x}, expected: e05e239e")

# What if we calculate CRC on modified bundle?
temp_out = r"C:\Users\oldga\.gemini\antigravity-ide\brain\ba94c348-943c-471c-a99f-190ed79432c3\scratch\test_output.bundle"
if os.path.exists(temp_out):
    with open(temp_out, "rb") as f:
        mod_data = f.read()
    crc_mod = zlib.crc32(mod_data)
    print(f"Modified bundle zlib.crc32: {crc_mod:08x}, expected from log: 4e121d11")
