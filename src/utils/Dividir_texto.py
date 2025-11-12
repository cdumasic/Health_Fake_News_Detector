import json
import numpy as np

# === CONFIGURACIÓN ===
input_path = "data/Text_to_back_translation/datos_baseline.json" #Dataset original
output_prefix = "data/Text_to_back_translation/datos_baseline_parte" #Prefijo de salida
num_parts = 3 #Cantidad de divisiones

# === CARGAR JSON ===
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# === DIVIDIR EN PARTES ===
splits = np.array_split(data, num_parts)

# === GUARDAR CADA PARTE ===
for i, part in enumerate(splits):
    output_path = f"{output_prefix}{i+1}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(part.tolist(), f, ensure_ascii=False, indent=2)
    print(f"✅ Guardado: {output_path} ({len(part)} registros)")