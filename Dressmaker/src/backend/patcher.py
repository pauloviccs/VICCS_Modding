import os
import shutil
import json
import subprocess
import time
import re
import struct
import UnityPy

DEFAULT_GAME_PATHS = [
    r"C:\Games\Dressmaker",
    r"C:\Program Files (x86)\Steam\steamapps\common\Dressmaker",
    r"D:\SteamLibrary\steamapps\common\Dressmaker",
    r"E:\SteamLibrary\steamapps\common\Dressmaker"
]

BUNDLE_NAME = "localization-string-tables-english(en)_assets_all.bundle"

BUNDLE_REL_PATH = os.path.join(
    "Dressmaker_Data", "StreamingAssets", "aa", "StandaloneWindows64",
    BUNDLE_NAME
)

CATALOG_REL_PATH = os.path.join(
    "Dressmaker_Data", "StreamingAssets", "aa", "catalog.bin"
)

MANIFEST_REL_PATH = os.path.join("Dressmaker_Data", "mod_manifest.json")
BACKUP_DIR_NAME = "_OriginalBackup"

class ModPatcher:
    def __init__(self, game_dir=None):
        self.game_dir = game_dir or self.detect_game_dir()

    def detect_game_dir(self):
        for path in DEFAULT_GAME_PATHS:
            if os.path.isdir(path) and os.path.isfile(os.path.join(path, "Dressmaker.exe")):
                return path
        return r"C:\Games\Dressmaker"

    def get_bundle_path(self):
        if not self.game_dir:
            return None
        return os.path.join(self.game_dir, BUNDLE_REL_PATH)

    def get_catalog_path(self):
        if not self.game_dir:
            return None
        return os.path.join(self.game_dir, CATALOG_REL_PATH)

    def get_backup_path(self):
        bundle_path = self.get_bundle_path()
        if not bundle_path:
            return None
        bundle_dir = os.path.dirname(bundle_path)
        backup_dir = os.path.join(bundle_dir, BACKUP_DIR_NAME)
        return os.path.join(backup_dir, os.path.basename(bundle_path))

    def get_catalog_backup_path(self):
        cat_path = self.get_catalog_path()
        if not cat_path:
            return None
        cat_dir = os.path.dirname(cat_path)
        backup_dir = os.path.join(cat_dir, BACKUP_DIR_NAME)
        return os.path.join(backup_dir, os.path.basename(cat_path))

    def get_manifest_path(self):
        if not self.game_dir:
            return None
        return os.path.join(self.game_dir, MANIFEST_REL_PATH)

    def is_game_valid(self):
        if not self.game_dir or not os.path.isdir(self.game_dir):
            return False
        exe_path = os.path.join(self.game_dir, "Dressmaker.exe")
        bundle_path = self.get_bundle_path()
        catalog_path = self.get_catalog_path()
        return os.path.isfile(exe_path) and os.path.isfile(bundle_path) and os.path.isfile(catalog_path)

    def is_game_running(self):
        try:
            output = subprocess.check_output('tasklist /FI "IMAGENAME eq Dressmaker.exe"', shell=True).decode('latin-1', errors='ignore')
            return "Dressmaker.exe" in output
        except Exception:
            return False

    def is_mod_installed(self):
        manifest_path = self.get_manifest_path()
        return os.path.isfile(manifest_path)

    def backup_exists(self):
        backup_file = self.get_backup_path()
        cat_backup = self.get_catalog_backup_path()
        return (backup_file is not None and os.path.isfile(backup_file)) and \
               (cat_backup is not None and os.path.isfile(cat_backup))

    def get_status(self):
        valid = self.is_game_valid()
        running = self.is_game_running()
        installed = self.is_mod_installed()
        has_backup = self.backup_exists()

        manifest_info = {}
        if installed:
            try:
                with open(self.get_manifest_path(), "r", encoding="utf-8") as f:
                    manifest_info = json.load(f)
            except Exception:
                pass

        return {
            "game_dir": self.game_dir,
            "is_valid": valid,
            "is_running": running,
            "is_installed": installed,
            "has_backup": has_backup,
            "manifest": manifest_info
        }

    def create_backup(self):
        bundle_path = self.get_bundle_path()
        backup_path = self.get_backup_path()
        catalog_path = self.get_catalog_path()
        catalog_backup = self.get_catalog_backup_path()

        if not bundle_path or not os.path.isfile(bundle_path):
            raise FileNotFoundError("Bundle original não encontrado para backup.")
        if not catalog_path or not os.path.isfile(catalog_path):
            raise FileNotFoundError("Catalog.bin original não encontrado para backup.")

        # Backup do bundle
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        if not os.path.isfile(backup_path):
            shutil.copy2(bundle_path, backup_path)

        # Backup do catalog.bin
        os.makedirs(os.path.dirname(catalog_backup), exist_ok=True)
        if not os.path.isfile(catalog_backup):
            shutil.copy2(catalog_path, catalog_backup)

        return backup_path

    def patch_catalog_crc(self, catalog_path):
        """Desativa a checagem de CRC no catalog.bin da Unity para o bundle traduzido."""
        with open(catalog_path, "rb") as f:
            cat_bytes = bytearray(f.read())

        pos = cat_bytes.find(BUNDLE_NAME.encode('latin-1'))
        if pos == -1:
            raise ValueError(f"Bundle {BUNDLE_NAME} não encontrado dentro de catalog.bin")

        sub = cat_bytes[pos:pos+250]
        hex_m = re.search(rb'[0-9a-f]{32}', sub)
        if not hex_m:
            raise ValueError("Hash hexadecimal do bundle não localizado no catalog.bin")

        hash_pos = pos + hex_m.start()
        crc_offset = hash_pos + 32 + 8
        # Zera os 4 bytes do CRC (CRC=0 instrui a Unity a ignorar verificação)
        cat_bytes[crc_offset:crc_offset+4] = b"\x00\x00\x00\x00"

        with open(catalog_path, "wb") as f:
            f.write(cat_bytes)

    def restore_original(self):
        if self.is_game_running():
            raise RuntimeError("O jogo Dressmaker está aberto. Feche o jogo antes de restaurar.")

        backup_path = self.get_backup_path()
        bundle_path = self.get_bundle_path()
        catalog_backup = self.get_catalog_backup_path()
        catalog_path = self.get_catalog_path()

        if not backup_path or not os.path.isfile(backup_path):
            raise FileNotFoundError("Nenhum backup de bundle encontrado para restauração.")

        # Restaura bundle
        shutil.copy2(backup_path, bundle_path)

        # Restaura catalog.bin se backup existir
        if catalog_backup and os.path.isfile(catalog_backup):
            shutil.copy2(catalog_backup, catalog_path)

        # Remove manifesto
        manifest_path = self.get_manifest_path()
        if os.path.isfile(manifest_path):
            try:
                os.remove(manifest_path)
            except Exception:
                pass

        return True

    def apply_patch(self, translations_dict, progress_callback=None):
        if not self.is_game_valid():
            raise RuntimeError("Diretório do jogo inválido ou arquivos não encontrados.")

        if self.is_game_running():
            raise RuntimeError("O jogo Dressmaker está aberto. Feche-o para instalar o mod.")

        if progress_callback:
            progress_callback(10, "Criando backup seguro dos arquivos originais...")
        
        # Garante backup original intocado do bundle e do catalog.bin
        self.create_backup()

        backup_path = self.get_backup_path()
        bundle_path = self.get_bundle_path()
        catalog_path = self.get_catalog_path()

        if progress_callback:
            progress_callback(25, "Lendo tabelas originais do jogo...")

        # Carrega a partir do backup para nunca acumular corrupções
        env = UnityPy.load(backup_path)
        patched_count = 0
        total_matched = 0

        if progress_callback:
            progress_callback(50, "Aplicando traduções em Português-Brasileiro...")

        for obj in env.objects:
            if obj.type.name == "MonoBehaviour":
                raw = obj.read_typetree()
                if isinstance(raw, dict) and "m_TableData" in raw:
                    table_modified = False
                    for item in raw["m_TableData"]:
                        item_id = str(item.get("m_Id"))
                        if item_id in translations_dict:
                            translated_text = translations_dict[item_id]
                            if item.get("m_Localized") != translated_text:
                                item["m_Localized"] = translated_text
                                patched_count += 1
                                table_modified = True
                            total_matched += 1
                    
                    if table_modified:
                        obj.save_typetree(raw)

        if progress_callback:
            progress_callback(75, "Empacotando o bundle traduzido com segurança...")

        # Salva o bundle modificado
        saved_bytes = env.file.save()
        with open(bundle_path, "wb") as f:
            f.write(saved_bytes)

        if progress_callback:
            progress_callback(85, "Ajustando integridade do Addressables Catalog (Bypass CRC)...")

        # Ajusta o catalog.bin para ignorar CRC
        self.patch_catalog_crc(catalog_path)

        if progress_callback:
            progress_callback(95, "Registrando manifesto do mod...")

        # Grava o manifesto
        manifest = {
            "mod_name": "Dressmaker PT-BR Localization",
            "version": "1.0.1",
            "installed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "strings_patched": patched_count,
            "total_matched": total_matched
        }
        with open(self.get_manifest_path(), "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        if progress_callback:
            progress_callback(100, f"Instalação concluída com sucesso! ({patched_count} textos traduzidos)")

        return manifest

    def launch_game(self):
        if not self.is_game_valid():
            raise RuntimeError("Jogo não encontrado.")
        exe_path = os.path.join(self.game_dir, "Dressmaker.exe")
        subprocess.Popen([exe_path], cwd=self.game_dir)
        return True
