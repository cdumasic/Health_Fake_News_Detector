import json

def reordenar_keys_json(nombre_archivo_entrada, nombre_archivo_salida=None):
    """
    Reasigna los valores de la clave '_key' de cada elemento del JSON,
    numerándolos consecutivamente desde 1 hasta n.

    Args:
        nombre_archivo_entrada (str): Ruta del archivo JSON de entrada.
        nombre_archivo_salida (str, opcional): Ruta donde guardar el archivo modificado.
            Si no se especifica, se sobrescribe el archivo original.

    Returns:
        bool: True si se realizó correctamente, False en caso de error.
    """
    try:
        with open(nombre_archivo_entrada, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        if not isinstance(datos, list):
            print("El archivo JSON no contiene una lista de objetos.")
            return False

        for i, elemento in enumerate(datos, start=1):
            if isinstance(elemento, dict):
                elemento["_key"] = i  # reasigna el número consecutivo

        if not nombre_archivo_salida:
            nombre_archivo_salida = nombre_archivo_entrada

        with open(nombre_archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)

        print(f"Las claves '_key' fueron actualizadas correctamente y guardadas en '{nombre_archivo_salida}'.")
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
nombre_archivo = 'data/Texto_filtro1/datos_aumentados_final_aleatorio.json'
salida = 'data/Texto_filtro1/datos_finales_aumentados.json'  # puedes dejarlo None para sobrescribir
reordenar_keys_json(nombre_archivo, salida)
