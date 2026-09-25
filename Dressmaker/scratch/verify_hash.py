import hashlib

with open(r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\catalog.bin", "rb") as f:
    cat_data = f.read()

print("MD5 of catalog.bin:", hashlib.md5(cat_data).hexdigest())
with open(r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\catalog.hash", "r") as f:
    print("In catalog.hash:   ", f.read().strip())
