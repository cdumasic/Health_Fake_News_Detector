import json

# Nombres de los archivos JSON que quieres combinar
archivos_json = [
    "data/Texto_filtro1/datos_baseline.json", 
    "data/Text_to_back_translation/datos_augmented.json", 
    "data/Text_to_synonyms/datos_synonyms.json"
]
archivo_salida = 'data/Texto_filtro1/datos_aumentados_final.json'

datos_combinados = []

# Leer cada archivo JSON y añadir sus datos a la lista
for nombre_archivo in archivos_json:
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            # Cargar el contenido del archivo
            datos = json.load(f)
            # Si los datos son una lista, añadirlos directamente
            if isinstance(datos, list):
                datos_combinados.extend(datos)
            # Si los datos son un objeto, añadirlo como un elemento más
            else:
                datos_combinados.append(datos)
    except FileNotFoundError:
        print(f"Error: El archivo {nombre_archivo} no fue encontrado.")
    except json.JSONDecodeError:
        print(f"Error: El archivo {nombre_archivo} no tiene un formato JSON válido.")

# Escribir los datos combinados en un nuevo archivo JSON
try:
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(datos_combinados, f, indent=4) # indent=4 para una buena legibilidad
    print(f"Archivos JSON combinados exitosamente en {archivo_salida}")
except Exception as e:
    print(f"Ocurrió un error al escribir el archivo de salida: {e}")