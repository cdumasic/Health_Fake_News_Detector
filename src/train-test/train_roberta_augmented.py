import json
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding,
)
from sklearn.model_selection import train_test_split
import evaluate
import torch

# Se añaden las rutas de los dataset de entrenamiento/validación y prueba
TRAIN_VAL_PATH = "./data/Texto_final/train_augmented.json"
TEST_PATH = "./data/Texto_final/test_augmented.json"

# Se añaden las rutas del modelo (ROBERTA) y las rutas de los resultados y el modelo entrenado
MODEL_NAME = "BSC-LT/mRoBERTa"
OUTPUT_DIR = "./resultados/roberta-fakenews-augmented-results"
MODEL_SAVE_DIR = "./modelos/roberta-fakenews-augmented-model"

#Se Carga y Preparación de los Datasets

def load_and_prepare_data(path, test_set=False):
    #Se carga renombra y mapea las etiquetas del JSON.
    df = pd.read_json(path)
    df = df.rename(columns={"text": "text", "label": "label"})
    df = df.dropna(subset=["text", "label"])
    
    # Convertir etiquetas a int
    if isinstance(df["label"].iloc[0], str):
        label_map = {"true": 1, "false": 0, "TRUE": 1, "FALSE": 0, "real": 1, "fake": 0}
        df["label"] = df["label"].map(label_map)
        
    return df

# Cargar ambos DataFrames
train_val_df = load_and_prepare_data(TRAIN_VAL_PATH)
test_df = load_and_prepare_data(TEST_PATH)

#Se divide del dataset 1 en Entrenamiento/Validación
#Se divide el 85% total en 70% Entrenamiento y 15% Validación
val_size_ratio_of_remaining = 0.15 / (0.70 + 0.15) 
train_df, val_df = train_test_split(
    train_val_df, 
    test_size=val_size_ratio_of_remaining, 
    stratify=train_val_df["label"], 
    random_state=42
)

#Se convertir a Datasets de Hugging Face
train_dataset = Dataset.from_pandas(train_df)
val_dataset = Dataset.from_pandas(val_df)
test_dataset = Dataset.from_pandas(test_df)

print(f"Tamaño de Entrenamiento: {len(train_dataset)}")
print(f"Tamaño de Validación: {len(val_dataset)}")
print(f"Tamaño de Prueba: {len(test_dataset)}")

#Se carga el modelo y se prepara para tokenizar
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

#Se tokeniza los datasets
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

train_dataset = train_dataset.map(tokenize_function, batched=True)
val_dataset = val_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True) # Tokenizar el dataset de prueba fijo

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Se eligen las métricas para la evaluación
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

# Se realiza la configuración del entrenamiento
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    load_best_model_at_end=True,
    metric_for_best_model="f1",
)

# Se entrena
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()

# Se evalua con el dataset de prueba
results = trainer.evaluate(eval_dataset=test_dataset)

print("\nResultados finales de las métricas con ROBERTA aumentados:")
for k, v in results.items():
    print(f"{k}: {v:.4f}")

model.save_pretrained(MODEL_SAVE_DIR)
tokenizer.save_pretrained(MODEL_SAVE_DIR)

# Se realiza un ejemplo de inferencia para comprobar los resultados del modelo
from transformers import pipeline

print(f"\nModelo guardado en {MODEL_SAVE_DIR}")

classifier = pipeline("text-classification", model=MODEL_SAVE_DIR, tokenizer=tokenizer)
example = "El Ministerio de Salud anunció una nueva campaña de vacunación en todo el país, la cúal será costará muchisimo dinero y será obligatoria para todos los Peruanos, una locura!!! ."
print("\nEjemplo de inferencia:")
print(classifier(example))


