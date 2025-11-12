import json
import math

def dividir_json(nombre_archivo, proporcion_85, proporcion_15):
    """
    Divide un archivo JSON (que contiene una lista) en dos archivos nuevos 
    con las proporciones especificadas.
    """
    # 1. Cargar los datos del archivo JSON
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    # Asegurarse de que los datos son una lista
    if not isinstance(datos, list):
        print("Error: El archivo JSON debe contener una lista de elementos en su raíz.")
        return

    # 2. Calcular el índice de división
    total_elementos = len(datos)
    indice_division = math.floor(total_elementos * proporcion_85) # Redondear hacia abajo para el índice

    # 3. Dividir la lista en dos partes
    parte_85_porciento = datos[:indice_division]  # Del inicio al índice de división (no incluido)
    parte_15_porciento = datos[indice_division:] # Del índice de división al final

    # 4. Guardar las nuevas listas en archivos JSON separados
    with open('datos_85_porciento.json', 'w', encoding='utf-8') as f_85:
        json.dump(parte_85_porciento, f_85, ensure_ascii=False, indent=4)

    with open('datos_15_porciento.json', 'w', encoding='utf-8') as f_15:
        json.dump(parte_15_porciento, f_15, ensure_ascii=False, indent=4)

    print(f"Original: {total_elementos} elementos")
    print(f"Parte 85% ({len(parte_85_porciento)} elementos) guardada en 'datos_85_porciento.json'")
    print(f"Parte 15% ({len(parte_15_porciento)} elementos) guardada en 'datos_15_porciento.json'")

# Uso del script
# Asegúrate de tener un archivo llamado 'tus_datos.json' en el mismo directorio
dividir_json('./data/Texto_final/data_augmented.json', 0.85, 0.15)
