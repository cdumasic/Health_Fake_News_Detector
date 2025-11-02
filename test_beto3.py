import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 1️⃣ Cargar modelo y tokenizer BETO
model_name = "dccuchile/bert-base-spanish-wwm-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 2️⃣ Leer el dataset JSON
dataset_path = "data/Texto_filtro1/data_limpia.json"

with open(dataset_path, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["text"] for item in data]
labels = [item.get("label", "unknown") for item in data]  # opcional

# 3️⃣ Tokenizar textos
inputs = tokenizer(
    texts,
    padding=True,
    truncation=True,
    return_tensors="pt",
    max_length=128
)

# 4️⃣ Inferencia (sin entrenamiento todavía)
with torch.no_grad():
    outputs = model(**inputs)

# 5️⃣ Obtener probabilidades
probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

# 6️⃣ Mostrar resultados
for i, text in enumerate(texts):
    prob_fake = probs[i][0].item()
    prob_real = probs[i][1].item()
    print(f"\n📰 Texto {i+1}:")
    print(f"{text[:120]}{'...' if len(text) > 120 else ''}")
    print(f"Probabilidad fake: {prob_fake:.4f} | real: {prob_real:.4f} | Label original: {labels[i]}")
