import os
import json
import UnityPy

DEFAULT_BUNDLE_PATH = r"C:\Games\Dressmaker\Dressmaker_Data\StreamingAssets\aa\StandaloneWindows64\localization-string-tables-english(en)_assets_all.bundle"

def extract_strings(bundle_path=DEFAULT_BUNDLE_PATH, output_json=None):
    if not os.path.exists(bundle_path):
        raise FileNotFoundError(f"Arquivo de bundle não encontrado: {bundle_path}")

    env = UnityPy.load(bundle_path)
    extracted_tables = []
    total_strings = 0

    for idx, obj in enumerate(env.objects):
        if obj.type.name == "MonoBehaviour":
            raw = obj.read_typetree()
            if isinstance(raw, dict) and "m_TableData" in raw:
                table_entries = []
                for item in raw["m_TableData"]:
                    table_entries.append({
                        "id": item.get("m_Id"),
                        "text": item.get("m_Localized", ""),
                        "metadata": item.get("m_Metadata", {})
                    })
                
                extracted_tables.append({
                    "table_index": idx,
                    "count": len(table_entries),
                    "entries": table_entries
                })
                total_strings += len(table_entries)

    result = {
        "source_bundle": bundle_path,
        "total_tables": len(extracted_tables),
        "total_strings": total_strings,
        "tables": extracted_tables
    }

    if output_json:
        os.makedirs(os.path.dirname(os.path.abspath(output_json)), exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return result

if __name__ == "__main__":
    out_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw_strings_en.json"))
    print(f"Extraindo strings para {out_file}...")
    res = extract_strings(output_json=out_file)
    print(f"Sucesso! {res['total_strings']} strings extraídas de {res['total_tables']} tabelas.")
