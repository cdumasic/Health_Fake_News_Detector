import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, DataCollatorWithPadding
import evaluate
import torch

# Se añaden las rutas del dataset de pruebas
MODEL_PATH = "./modelos/beto-fakenews-baseline-model"
NEW_TEST_DATA_PATH = "./data/Texto_final/test_baseline.json" 

# Se carga el dataset de pruebas
df_test = pd.read_json(NEW_TEST_DATA_PATH)
df_test = df_test.rename(columns={"text": "text", "label": "label"})

label_map = {"true": 1, "false": 0, "TRUE": 1, "FALSE": 0}
df_test["label"] = df_test["label"].map(label_map)
test_dataset = Dataset.from_pandas(df_test)

# Se carga el modelo guardado y el tokenizador
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Se tokeniza el dataset de pruebas
def tokenize_function(examples):
    # Se usa la misma configuración de tokenización
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

test_dataset = test_dataset.map(tokenize_function, batched=True)

# Se definen las métricas
accuracy = evaluate.load("accuracy")
f1 = evaluate.load("f1")
precision = evaluate.load("precision")
recall = evaluate.load("recall")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = torch.argmax(torch.tensor(logits), dim=-1)
    return {
        "accuracy": accuracy.compute(predictions=predictions, references=labels)["accuracy"],
        "f1": f1.compute(predictions=predictions, references=labels)["f1"],
        "precision": precision.compute(predictions=predictions, references=labels)["precision"],
        "recall": recall.compute(predictions=predictions, references=labels)["recall"],
    }

# Se crear un pequeño entrenador que verifica el modelo
trainer = Trainer(
    model=model,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

# Se evalua el modelo con el conjunto de pruebas
results = trainer.evaluate(eval_dataset=test_dataset)

print("\nResultados de la prueba:")
for k, v in results.items():
    print(f"{k}: {v:.4f}")