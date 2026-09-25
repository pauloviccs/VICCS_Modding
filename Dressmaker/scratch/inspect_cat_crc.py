cat_path = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\catalog.bin"
with open(cat_path, "rb") as f:
    data = f.read()

pos = 6055
print("Bytes around 6055:")
print(data[pos-20:pos+30].hex())

# Let's see what objects / strings are around 6055
print("Raw around 6055:")
print(data[pos-50:pos+50])
