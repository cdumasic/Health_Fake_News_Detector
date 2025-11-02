import os
import json

def corregir_tildes_simbolos(texto_con_simbolos):
    """
    Realiza las sustituciones de vocal+símbolo por la vocal acentuada correcta.
    """
    
    # Mapeo de sustitución (Patrones de error de codificación UTF-8/Latin-1)
    mapeos_originales = {
        # Caracteres de 2+ bytes
        "Ã¡": "á", "Ã©": "é", "Ã³": "ó", "Ãº": "ú",
        "Ã": "Á", "Ã‰": "É", "Ã": "Í", "Ã“": "Ó", "Ãš": "Ú",
        "Ã‘": "Ñ", 
        "Â¿": "¿", "Â«": "«", "Â»": "»", "Â¡": "¡", "â€˜": "'",
        "â€”": "”", "â€”":"”", "â€¦" : "", "â€“":",","â€¢":"-", "â€¯°":"°",
        "Ã±": "ñ", "â€œ": "\"", "â€": "\"", "â€™": "'", 
        
        # Caracteres de 1 byte (Deben ir al final si se usa un diccionario simple)
        "Ã": "í", "Â": "",
    }
    
    # Ordenar los mapeos por longitud descendente para evitar sustituciones parciales
    mapeos_ordenados = sorted(
        mapeos_originales.items(), 
        key=lambda item: len(item[0]), 
        reverse=True
    )
    
    texto_corregido = texto_con_simbolos
    for simbolo, tilde in mapeos_ordenados:
        texto_corregido = texto_corregido.replace(simbolo, tilde)
        
    return texto_corregido


def corregir_json_recursivo(data):
    """
    Función recursiva para recorrer un objeto JSON (diccionario o lista) 
    y aplicar la corrección de tildes a todas las cadenas de texto encontradas.
    """
    if isinstance(data, dict):
        # Si es un diccionario, recorre sus claves y valores
        return {k: corregir_json_recursivo(v) for k, v in data.items()}
    elif isinstance(data, list):
        # Si es una lista, recorre cada elemento
        return [corregir_json_recursivo(elem) for elem in data]
    elif isinstance(data, str):
        # Si es una cadena de texto, aplica la corrección
        return corregir_tildes_simbolos(data)
    else:
        # Devuelve cualquier otro tipo de dato sin cambios (números, booleanos, null)
        return data


def procesar_archivo_json(archivo_entrada, archivo_salida):
    """
    Lee un archivo JSON, corrige recursivamente las tildes dentro de las cadenas
    de texto y escribe el nuevo JSON limpio.
    """
    
    # 1. Leer y cargar el JSON
    data_original = None
    try:
        # Abrimos el JSON. Usamos 'utf-8' pero agregamos errors='ignore' 
        # para que pueda cargar el contenido aunque haya errores de codificación
        # en la lectura inicial (el paso de sustitución lo arreglará).
        with open(archivo_entrada, 'r', encoding='utf-8', errors='ignore') as f_in:
            contenido_bruto = f_in.read()
            data_original = json.loads(contenido_bruto)
            print(f"✅ Archivo JSON de entrada '{archivo_entrada}' leído y cargado correctamente.")
            
    except FileNotFoundError:
        print(f"❌ ERROR: No se encontró el archivo de entrada '{archivo_entrada}'.")
        return
    except json.JSONDecodeError as e:
        print(f"❌ ERROR de formato JSON: El archivo no es un JSON válido. {e}")
        return
    except Exception as e:
        print(f"❌ ERROR al leer el archivo: {e}")
        return

    # 2. Corregir el contenido (recursivamente en todo el objeto)
    print("⏳ Aplicando correcciones de tildes...")
    data_corregida = corregir_json_recursivo(data_original)
    
    # 3. Escribir el archivo de salida
    try:
        # Usar json.dump para escribir el objeto corregido.
        # 'indent=4' para que el JSON de salida sea legible.
        with open(archivo_salida, 'w', encoding='utf-8') as f_out:
            json.dump(data_corregida, f_out, ensure_ascii=False, indent=4)
            print(f"✅ Archivo de salida '{archivo_salida}' creado con éxito.")
            print("¡Proceso de limpieza JSON finalizado!")
            
    except Exception as e:
        print(f"❌ ERROR al escribir el archivo: {e}")
        
# --- Configuración y Ejecución ---

# Asegúrate de que estas rutas apuntan a tus archivos JSON
ARCHIVO_ENTRADA = 'data/Texto_filtro1/datos.json' 
ARCHIVO_SALIDA = 'data/Texto_filtro1/data_limpia.json'

# Iniciar el proceso
procesar_archivo_json(ARCHIVO_ENTRADA, ARCHIVO_SALIDA)
