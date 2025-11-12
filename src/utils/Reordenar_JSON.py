import json

def mover_contenido_etiquetas(archivo_json):
    """
    Carga un archivo JSON, mueve el contenido de 'text2' a 'text1'
    y vacía 'text2', luego sobrescribe el archivo original.

    Args:
        archivo_json (str): Ruta al archivo JSON.
    """
    try:
        # 1. Leer el archivo JSON
        with open(archivo_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        # 2. Verificar si las etiquetas existen y realizar la modificación
        if "borrar" in datos and "text" in datos:
            # Mover el valor de text2 a text1
            datos["borrar"] = datos["text"]
            # Vaciar text2
            datos["text"] = ""
            print("Datos modificados en memoria.")
        else:
            print("Error: No se encontraron las etiquetas 'borrar' o 'text' en el JSON.")
            return

        # 3. Sobrescribir el archivo original con los datos modificados
        with open(archivo_json, 'w', encoding='utf-8') as f:
            # Usamos indent=4 para mantener el formato legible
            json.dump(datos, f, ensure_ascii=False, indent=4)
        
        print(f"Archivo '{archivo_json}' sobrescrito exitosamente.")

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_json}' no fue encontrado.")
    except json.JSONDecodeError:
        print(f"Error: No se pudo decodificar el archivo JSON. Asegúrate de que el formato sea válido.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    # Nombre del archivo a modificar
    nombre_del_archivo = "data/Text_to_back_translation/datos_augmented.json"
    
    # --- PASO 1: Crear un archivo de prueba inicialmente ---
    datos_iniciales = {
        "_key": "6666666",
        "borrar": "Hola",
        "label": "TRUE",
        "text": "Hola a todos"
    }
    with open(nombre_del_archivo, 'w', encoding='utf-8') as f:
        json.dump(datos_iniciales, f, indent=4)
    print(f"Archivo de prueba '{nombre_del_archivo}' creado inicialmente.\n")
    
    # --- PASO 2: Ejecutar la función para modificarlo ---
    mover_contenido_etiquetas(nombre_del_archivo)