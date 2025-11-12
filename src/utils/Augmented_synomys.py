import json
import random
import spacy
from transformers import pipeline
from tqdm import tqdm

# 1️⃣ Cargar spaCy para español
nlp = spacy.load("es_core_news_md")

# 2️⃣ Cargar el modelo BETO para "fill-mask"
fill_mask = pipeline("fill-mask", model="dccuchile/bert-base-spanish-wwm-cased", top_k=3)

# 3️⃣ Parámetros de configuración
MASK_TOKEN = tokenizer_mask = fill_mask.tokenizer.mask_token  # normalmente [MASK]
REPLACE_POS = {"NOUN", "ADJ", "VERB"}  # categorías a reemplazar
REPLACE_PROB = 0.15  # probabilidad de reemplazar una palabra
INPUT_FILE = "data/Text_to_synonyms/datos_baseline_parte3.json"
OUTPUT_FILE = "data/Text_to_synonyms/datos_synonyms_parte3.json"

def augment_text(text):
    """Reemplaza palabras por sinónimos contextuales con BETO."""
    doc = nlp(text)
    new_tokens = []

    for token in doc:
        if token.pos_ in REPLACE_POS and random.random() < REPLACE_PROB:
            masked_sentence = text.replace(token.text, MASK_TOKEN, 1)
            try:
                preds = fill_mask(masked_sentence)
                if preds:
                    # Elegimos aleatoriamente entre las 2 mejores predicciones
                    replacement = random.choice(preds[:2])["token_str"].strip()
                    new_tokens.append(replacement)
                    continue
            except Exception:
                pass
        new_tokens.append(token.text)

    return " ".join(new_tokens)

def main():
    print("🔹 Cargando dataset:", INPUT_FILE)
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    augmented_data = []
    for item in tqdm(data, desc="Generando textos aumentados"):
        new_text = augment_text(item["text"])
        augmented_data.append({
            "text": new_text,
            "label": item["label"],
            "source": "contextual_augmentation"
        })

    print("💾 Guardando resultados en", OUTPUT_FILE)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(augmented_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Proceso completado. Se generaron {len(augmented_data)} textos aumentados.")

if __name__ == "__main__":
    main()
