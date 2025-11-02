import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# 1️⃣ Modelo y tokenizer BETO
model_name = "dccuchile/bert-base-spanish-wwm-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 2️⃣ Carpeta donde están los textos
data_dir = "data/Texto_filtro1"

texts = []
file_names = []

# 3️⃣ Leer todos los archivos de texto
for file_name in os.listdir(data_dir):
    if file_name.endswith(".txt"):
        path = os.path.join(data_dir, file_name)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()
            texts.append(text)
            file_names.append(file_name)

# 4️⃣ Tokenizar
inputs = tokenizer(
    texts,
    padding=True,
    truncation=True,
    return_tensors="pt",
    max_length=128
)

# 5️⃣ Pasar los textos por el modelo
with torch.no_grad():
    outputs = model(**inputs)

# 6️⃣ Calcular probabilidades
probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

# 7️⃣ Mostrar resultados
for i, name in enumerate(file_names):
    print(f"\nArchivo: {name}")
    print(f"Probabilidades (clase 0=fake, clase 1=real): {probs[i].tolist()}")
