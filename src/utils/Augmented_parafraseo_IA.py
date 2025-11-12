import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm import tqdm
import torch

# ===============================
# CONFIGURACIÓN DEL MODELO
# ===============================
MODEL_NAME = "unicamp-dl/mt5-base-multilingual-paraphraser"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(DEVICE)

# ===============================
# PARÁMETROS
# ===============================
INPUT_JSON = "data/Text_to_paraphrase/datos_baseline_parte1.json"    # tu dataset base
OUTPUT_JSON = "data/Text_to_paraphrase/datos_paraphrased_parte1.json"
NUM_PARAPHRASES = 2                     # cuántas versiones generar por texto
MAX_LENGTH = 128                        # límite de tokens

# ===============================
# FUNCIÓN DE PARAFRASEO
# ===============================
def paraphrase_text(text, num_return_sequences=2):
    """Genera reformulaciones del texto usando mT5."""
    input_text = f"paraphrase: {text} </s>"
    encoding = tokenizer(
        input_text,
        max_length=MAX_LENGTH,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    ).to(DEVICE)

    outputs = model.generate(
        **encoding,
        max_length=MAX_LENGTH,
        num_beams=4,
        num_return_sequences=num_return_sequences,
        temperature=1.5,
        top_p=0.95,
        top_k=50,
        do_sample=True
    )

    paraphrases = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    return paraphrases

# ===============================
# PROCESAMIENTO DEL JSON
# ===============================
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

augmented_data = []

print(f"🔁 Generando parafraseos con mT5 en {DEVICE.upper()}...\n")

for item in tqdm(data, desc="Procesando textos"):
    text = item["text"]
    label = item["label"]

    try:
        new_texts = paraphrase_text(text, num_return_sequences=NUM_PARAPHRASES)
        for new_text in new_texts:
            augmented_data.append({"text": new_text, "label": label})
    except Exception as e:
        print(f"⚠️ Error con texto: {text[:50]}... ({e})")

# Combinar original + aumentado
final_data = augmented_data

# ===============================
# GUARDAR RESULTADO
# ===============================
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Aumento completado. Total ejemplos: {len(final_data)}")
print(f"📁 Archivo guardado: {OUTPUT_JSON}")
