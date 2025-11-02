from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# 1️⃣ Cargar el tokenizer y el modelo BETO
model_name = "dccuchile/bert-base-spanish-wwm-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 2️⃣ Texto de prueba (puedes cambiarlo por uno tuyo)
def procesar_archivo_texto(archivo_entrada, contenido_original):
    """
    Lee el contenido del archivo_entrada, corrige las tildes y lo escribe
    en el archivo_salida.
    """
    try:
        # --- 1. Leer el archivo de entrada ---
        # 'r' para modo lectura, 'utf-8' es crucial para manejar tildes y símbolos
        with open(archivo_entrada, 'r', encoding='utf-8') as f_in:
            contenido_original = f_in.read()
            print(f"✅ Archivo de entrada '{archivo_entrada}' leído correctamente.")
            
    except FileNotFoundError:
        print(f"❌ ERROR: No se encontró el archivo de entrada '{archivo_entrada}'.")
        print("Asegúrate de que el archivo exista en la misma carpeta que el script.")
        return
    except Exception as e:
        print(f"❌ ERROR al leer el archivo: {e}")
        return

texts = [
    "La vacuna contra el COVID-19 contiene microchips para controlar a las personas.",
    "El Ministerio de Salud recomienda la vacunación para prevenir enfermedades."
]

# 3️⃣ Tokenizar los textos
inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=128)

# 4️⃣ Pasar los textos por el modelo
with torch.no_grad():
    outputs = model(**inputs)

# 5️⃣ Ver los logits (valores sin entrenar)
print("Logits sin entrenar:")
print(outputs.logits)

# 6️⃣ Convertirlos a probabilidades con softmax
probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
print("\nProbabilidades estimadas:")
print(probs)