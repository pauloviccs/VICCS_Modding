import os

FRONTEND_DIR = os.path.abspath(os.path.join("src", "backend", "..", "frontend"))
rel_path = "index.html"
file_path = os.path.abspath(os.path.join(FRONTEND_DIR, rel_path))

print(f"FRONTEND_DIR: {FRONTEND_DIR}")
print(f"file_path: {file_path}")
print(f"file exists: {os.path.isfile(file_path)}")
print(f"startswith: {file_path.startswith(FRONTEND_DIR)}")
