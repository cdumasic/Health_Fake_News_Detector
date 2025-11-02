import json
import torch
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
    pipeline
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# ===============================================================
# 1. CONFIGURACIÓN
# ===============================================================
MODEL_NAME = "dccuchile/bert-base-spanish-wwm-cased"
DATA_PATH = "data/Texto_filtro1/datos_limpios.json"
MAX_LENGTH = 128
NUM_LABELS = 2  # fake / real

# ===============================================================
# 2. CARGAR DATASET
# ===============================================================
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["text"] for item in data]
labels_text = [item["label"] for item in data]

# Mapear etiquetas a números
# Normalizar etiquetas a minúsculas y sin espacios
labels_clean = [l.strip().lower() for l in labels_text]

# Mapear según las variantes posibles
label_map = {
    "false": 0,
    "true": 1
}

try:
    labels = [label_map[l] for l in labels_clean]
except KeyError as e:
    print(f"Etiqueta desconocida encontrada: {e}")
    print("Revisa tu JSON. Solo se aceptan false y true.")
    raise

# Dividir train/validation
train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

# ===============================================================
# 3. TOKENIZACIÓN
# ===============================================================
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize_function(batch):
    return tokenizer(
        batch["text"],
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH
    )

# Crear datasets de Hugging Face
train_dataset = Dataset.from_dict({"text": train_texts, "label": train_labels})
val_dataset = Dataset.from_dict({"text": val_texts, "label": val_labels})

# Tokenizar datasets
train_dataset = train_dataset.map(tokenize_function, batched=True)
val_dataset = val_dataset.map(tokenize_function, batched=True)

# ===============================================================
# 4. MODELO
# ===============================================================
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=NUM_LABELS)

# ===============================================================
# 5. MÉTRICAS
# ===============================================================
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = torch.argmax(torch.tensor(logits), dim=-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="binary")
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}

# ===============================================================
# 6. ENTRENAMIENTO
# ===============================================================
training_args = TrainingArguments(
    output_dir="./beto-fakenews-results",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    logging_dir="./logs",
    logging_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
    compute_metrics=compute_metrics
)

trainer.train()

# ===============================================================
# 7️⃣ EVALUACIÓN FINAL
# ===============================================================
metrics = trainer.evaluate()
print("\n📊 Resultados finales:")
for key, value in metrics.items():
    print(f"{key}: {value:.4f}")

# ===============================================================
# 8️⃣ GUARDAR MODELO
# ===============================================================
trainer.save_model("./beto-fakenews-model")
tokenizer.save_pretrained("./beto-fakenews-model")

print("\nModelo guardado en ./beto-fakenews-model")

# ===============================================================
# 9️⃣ PRUEBA RÁPIDA (opcional)
# ===============================================================
print("\nEjemplo de inferencia:")
clf = pipeline("text-classification", model="./beto-fakenews-model", tokenizer=tokenizer)

test_text = "El Ministerio de Salud recomienda usar mascarilla en hospitales."
print(clf(test_text))
