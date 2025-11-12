import torch
from transformers import MarianMTModel, MarianTokenizer
import json
from tqdm import tqdm
import os

# === CONFIGURACIÓN ===
input_files = [
    "data/Text_to_back_translation/datos_baseline_parte1.json", 
    "data/Text_to_back_translation/datos_baseline_parte2.json", 
    "data/Text_to_back_translation/datos_baseline_parte3.json"
]
src_lang = "es"
mid_lang = "en"
batch_size = 4  # Ideal para MX350

# === SELECCIONAR DISPOSITIVO ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🖥️ Usando dispositivo: {device}")

# === CARGAR MODELOS ===
model_name_src = f"Helsinki-NLP/opus-mt-{src_lang}-{mid_lang}"
model_name_mid = f"Helsinki-NLP/opus-mt-{mid_lang}-{src_lang}"

tokenizer_src = MarianTokenizer.from_pretrained(model_name_src)
model_src = MarianMTModel.from_pretrained(model_name_src).to(device)

tokenizer_mid = MarianTokenizer.from_pretrained(model_name_mid)
model_mid = MarianMTModel.from_pretrained(model_name_mid).to(device)

# === FUNCIÓN PARA TRADUCIR LOTES ===
def translate_batch(texts, tokenizer, model):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=256).to(device)
    translated = model.generate(**inputs, max_length=256)
    return [tokenizer.decode(t, skip_special_tokens=True) for t in translated]

# === FUNCIÓN PRINCIPAL DE BACK TRANSLATION ===
def back_translate_batch(texts):
    try:
        mid_texts = translate_batch(texts, tokenizer_src, model_src)
        back_texts = translate_batch(mid_texts, tokenizer_mid, model_mid)
        return back_texts
    except Exception as e:
        print(f"⚠️ Error traduciendo lote: {e}")
        return texts

# === PROCESAR ARCHIVOS ===
for file in input_files:
    if not os.path.exists(file):
        print(f"⛔ Archivo no encontrado: {file}")
        continue

    print(f"\n📖 Procesando {file}...")
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [item["text"] for item in data if "text" in item]
    augmented_texts = []

    for i in tqdm(range(0, len(texts), batch_size), desc=f"Traduciendo {file}"):
        batch = texts[i:i+batch_size]
        new_texts = back_translate_batch(batch)
        augmented_texts.extend(new_texts)

        # Limpiar VRAM
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    # Asignar textos aumentados
    for i, item in enumerate(data):
        if i < len(augmented_texts):
            item["augmented_text"] = augmented_texts[i]

    # Guardar archivo nuevo
    output_path = file.replace(".json", "_augmented.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Guardado: {output_path} ({len(data)} registros)")