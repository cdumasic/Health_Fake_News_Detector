import json
import random

def aletorizar_json(nombre_archivo_entrada, nombre_archivo_salida=None):
    """
    Barajea (aleatoriza) el orden de los elementos en un archivo JSON de tipo lista.
    
    Args:
        nombre_archivo_entrada (str): Ruta del archivo JSON original.
        nombre_archivo_salida (str, opcional): Ruta donde guardar el JSON barajeado.
            Si no se especifica, se sobrescribe el archivo original.
    
    Returns:
        bool: True si se realizó correctamente, False si ocurrió un error.
    """
    try:
        with open(nombre_archivo_entrada, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        if not isinstance(datos, list):
            print("El archivo JSON no contiene una lista, no se puede barajear.")
            return False

        random.shuffle(datos)  # <- mezcla los elementos de la lista

        # Si no se da nombre de salida, sobrescribe el archivo original
        if not nombre_archivo_salida:
            nombre_archivo_salida = nombre_archivo_entrada

        with open(nombre_archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)

        print(f"Archivo barajeado correctamente y guardado en '{nombre_archivo_salida}'.")
        return True

    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo_entrada}' no fue encontrado.")
        return False
    except json.JSONDecodeError:
        print(f"Error: El archivo '{nombre_archivo_entrada}' no contiene JSON válido.")
        return False
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return False


# --- Ejemplo de uso ---
nombre_archivo = './data/Texto_filtro1/datos_aumentados_final.json'
salida = './data/Texto_filtro1/datos_aumentados_final_aleatorio.json'  # puedes dejarlo None para sobrescribir
aletorizar_json(nombre_archivo, salida)
