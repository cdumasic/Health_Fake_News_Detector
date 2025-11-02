import os

def corregir_tildes_simbolos(texto_con_simbolos):
    """
    Realiza las sustituciones de vocal+símbolo por la vocal acentuada correcta.
    """
    
    # Mapeo de sustitución (puedes añadir o cambiar símbolos según tu necesidad)
    mapeos = {
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
    
    texto_corregido = texto_con_simbolos
    for simbolo, tilde in mapeos.items():
        # Utilizamos replace para sustituir todas las ocurrencias
        texto_corregido = texto_corregido.replace(simbolo, tilde)
        
    return texto_corregido


def procesar_archivo_texto(archivo_entrada, archivo_salida):
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

    # --- 2. Corregir el contenido ---
    contenido_corregido = corregir_tildes_simbolos(contenido_original)
    
    # --- 3. Escribir el archivo de salida ---
    try:
        # 'w' para modo escritura (sobrescribirá si ya existe), 'utf-8' para mantener tildes
        with open(archivo_salida, 'w', encoding='utf-8') as f_out:
            f_out.write(contenido_corregido)
            print(f"✅ Archivo de salida '{archivo_salida}' creado con éxito.")
            print("¡Proceso finalizado!")
            
    except Exception as e:
        print(f"❌ ERROR al escribir el archivo: {e}")
        
# --- Configuración y Ejecución ---

ARCHIVO_ENTRADA = 'data/Texto_base/data3.txt' 
ARCHIVO_SALIDA = 'data/Texto_filtro1/data3.txt'

# Iniciar el proceso
procesar_archivo_texto(ARCHIVO_ENTRADA, ARCHIVO_SALIDA)