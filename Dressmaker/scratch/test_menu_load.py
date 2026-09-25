import os
import subprocess
import time

game_dir = r"C:\Games\Dressmaker"
print("Iniciando Dressmaker.exe por 12 segundos...")
proc = subprocess.Popen([os.path.join(game_dir, "Dressmaker.exe")], cwd=game_dir)
time.sleep(12)
proc.terminate()
time.sleep(1)

log_path = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\Cozy Lives\Dressmaker\Player.log")
with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

print(f"Tamanho do log: {len(content)} caracteres")
print("\n--- Conteúdo do Player.log ---")
print(content)
