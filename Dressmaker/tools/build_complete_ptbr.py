import os
import json
import time
import re
import urllib.request
import urllib.parse

RAW_JSON = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw_strings_en.json"))
OUTPUT_JSON = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "translations_ptbr.json"))

# Termos de alta alfaiataria e interface com garantia de perfeição
CURATED_TERMS = {
    # Tags e estilos
    "Professional": "Profissional",
    "Casual": "Casual",
    "Cool": "Fresco",
    "Cute": "Fofo",
    "Daywear": "Dia a Dia",
    "Eclectic": "Eclético",
    "Elaborate": "Elaborado",
    "Elegant": "Elegante",
    "Eveningwear": "Traje de Noite",
    "Flowers": "Floral",
    "Formal": "Formal",
    "Glamour": "Glamour",
    "Gothic": "Gótico",
    "Patterned": "Estampado",
    "Playful": "Divertido",
    "Risqué": "Ousado",
    "Romantic": "Romântico",
    "Shimmering": "Cintilante",
    "Simple": "Simples",
    "Uncomfortable": "Desconfortável",
    "Warm": "Quente",
    "Workwear": "Trabalho",
    
    # Controles de costura
    "Sew": "Costurar",
    "Rotate": "Girar",
    "Change Speed": "Velocidade",
    "Reset": "Redefinir",
    
    # Modelagem e Peças
    "No Collar": "Sem Gola",
    "No Sleeves": "Sem Mangas",
    "Square Bodice": "Corpete Quadrado",
    "Cap Sleeve": "Manga Copinho",
    "Bias Cut Skirt": "Saia em Corte Viés",
    "Librarian Workwear": "Traje de Bibliotecária",
    "Rose needs a dress for work.": "Rose precisa de um vestido para o trabalho."
}

def clean_tailor_terms(text):
    # Correções específicas de gírias e falsos cognatos de alfaiataria
    corrections = [
        (r'\bsem coleira\b', 'sem gola'),
        (r'\bSem coleira\b', 'Sem Gola'),
        (r'\bmanga de boné\b', 'manga copinho'),
        (r'\bManga de boné\b', 'Manga Copinho'),
        (r'\bcorpete\b', 'corpete'),
        (r'\bcoleira\b', 'gola'),
        (r'\bColeira\b', 'Gola'),
    ]
    for pattern, repl in corrections:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text

def translate_batch(texts):
    if not texts:
        return []
    
    # Se for apenas 1 item
    if len(texts) == 1:
        txt = texts[0]
        if txt in CURATED_TERMS:
            return [CURATED_TERMS[txt]]
        return [translate_single_text(txt)]

    # Filtra curados previamente
    result_map = {}
    pending_to_send = []
    for t in texts:
        if t in CURATED_TERMS:
            result_map[t] = CURATED_TERMS[t]
        else:
            pending_to_send.append(t)

    if pending_to_send:
        # Usa separador exclusivo
        sep = "\n---DIV---\n"
        payload = sep.join(pending_to_send)
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=pt&dt=t&q=" + urllib.parse.quote(payload)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                full_text = "".join([part[0] for part in data[0] if part[0]])
            parts = full_text.split("---DIV---")
            if len(parts) == len(pending_to_send):
                for orig, trans in zip(pending_to_send, parts):
                    result_map[orig] = clean_tailor_terms(trans.strip())
            else:
                # Se o separador desalinhar, traduz um a um de forma segura
                for orig in pending_to_send:
                    result_map[orig] = clean_tailor_terms(translate_single_text(orig))
        except Exception:
            for orig in pending_to_send:
                result_map[orig] = clean_tailor_terms(translate_single_text(orig))

    return [result_map.get(t, t) for t in texts]

def translate_single_text(text):
    if not text or not text.strip():
        return text
    if text in CURATED_TERMS:
        return CURATED_TERMS[text]

    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=pt&dt=t&q=" + urllib.parse.quote(text)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                res = "".join([part[0] for part in data[0] if part[0]])
                return clean_tailor_terms(res.strip())
        except Exception:
            time.sleep(0.3 * (attempt + 1))
    return text

def run_translation_pipeline():
    print("=== Iniciando Pipeline de Tradução Completa (100% dos Textos) ===")
    with open(RAW_JSON, "r", encoding="utf-8") as f:
        raw = json.load(f)

    # Carrega traduções existentes
    translations = {}
    if os.path.exists(OUTPUT_JSON):
        with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
            translations = json.load(f)

    print(f"Traduções já consolidadas: {len(translations)}")

    # Mapeia todas as entradas
    all_entries = []
    for table_idx, table in enumerate(raw["tables"]):
        for e in table["entries"]:
            all_entries.append((table_idx, str(e["id"]), e["text"].strip()))

    print(f"Total de strings no jogo: {len(all_entries)}")

    # Descobre textos únicos que faltam traduzir
    pending_unique = set()
    for table_idx, str_id, txt in all_entries:
        if str_id not in translations and txt:
            if txt in CURATED_TERMS:
                translations[str_id] = CURATED_TERMS[txt]
            else:
                pending_unique.add(txt)

    pending_list = sorted(list(pending_unique))
    print(f"Textos únicos a traduzir em lotes: {len(pending_list)}")

    BATCH_SIZE = 35
    text_cache = {}
    processed = 0

    for i in range(0, len(pending_list), BATCH_SIZE):
        batch = pending_list[i:i+BATCH_SIZE]
        results = translate_batch(batch)
        for orig, trans in zip(batch, results):
            text_cache[orig] = trans
        processed += len(batch)
        print(f"Progresso: {processed}/{len(pending_list)} ({processed*100//len(pending_list)}%)...")

        # Checkpoint a cada 3 lotes
        if i % (BATCH_SIZE * 3) == 0:
            for table_idx, str_id, orig_txt in all_entries:
                if str_id not in translations and orig_txt in text_cache:
                    translations[str_id] = text_cache[orig_txt]
            with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
                json.dump(translations, f, ensure_ascii=False, indent=2)

    # Consolida tudo
    for table_idx, str_id, orig_txt in all_entries:
        if str_id not in translations and orig_txt in text_cache:
            translations[str_id] = text_cache[orig_txt]

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

    print(f"\n>>> CONCLUÍDO! {len(translations)} strings traduzidas salvas em {OUTPUT_JSON} <<<")

if __name__ == "__main__":
    run_translation_pipeline()
