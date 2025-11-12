import json

def contar_elementos_json(nombre_archivo):
    """
    Cuenta la cantidad de elementos en un archivo JSON y muestra
    cuántos tienen el campo 'label' con valor 'TRUE' o 'FALSE'.

    Args:
        nombre_archivo (str): La ruta al archivo JSON.

    Returns:
        dict: Un diccionario con el conteo total y los conteos por label.
        None: Si ocurre un error al leer el archivo.
    """
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)

            if isinstance(datos, list):
                total = len(datos)
                conteo_true = 0
                conteo_false = 0

                for elemento in datos:
                    if isinstance(elemento, dict) and 'label' in elemento:
                        valor = str(elemento['label']).strip().upper()
                        if valor == 'TRUE':
                            conteo_true += 1
                        elif valor == 'FALSE':
                            conteo_false += 1

                print(f"Total de elementos: {total}")
                print(f"Label = TRUE: {conteo_true}")
                print(f"Label = FALSE: {conteo_false}")

                return {
                    "total": total,
                    "true": conteo_true,
                    "false": conteo_false
                }

            elif isinstance(datos, dict):
                total = len(datos)
                print(f"El archivo contiene un diccionario con {total} claves principales.")
                return {"total": total}

            else:
                print(f"El archivo '{nombre_archivo}' no contiene un array o diccionario principal.")
                return None

    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo '{nombre_archivo}' no contiene JSON válido.")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None


# --- Ejemplo de uso ---
nombre_del_archivo = '../../data/Texto_filtro1/data_limpia.json'  # Reemplaza con el nombre de tu archivo
resultados = contar_elementos_json(nombre_del_archivo)

if resultados:
    print(f"\nResumen general del archivo '{nombre_del_archivo}':")
    print(resultados)
