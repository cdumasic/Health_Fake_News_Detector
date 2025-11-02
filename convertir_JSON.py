import pandas as pd
import os

def convertir_a_json(archivo_entrada, archivo_salida):
    """
    Convierte datos de un archivo CSV o XLSX a un archivo JSON.
    
    :param archivo_entrada: Ruta al archivo de entrada (.csv o .xlsx).
    :param archivo_salida: Ruta al archivo de salida (.json).
    """
    # 1. Verificar la existencia del archivo de entrada
    if not os.path.exists(archivo_entrada):
        print(f"❌ ERROR: El archivo de entrada '{archivo_entrada}' no existe.")
        return

    # 2. Determinar el tipo de archivo y leerlo
    try:
        if archivo_entrada.endswith('.csv'):
            # Leer el archivo CSV en un DataFrame de pandas
            df = pd.read_csv(archivo_entrada)
            print(f"✅ Archivo '{archivo_entrada}' (CSV) leído con éxito.")
        elif archivo_entrada.endswith('.xlsx'):
            # Leer el archivo XLSX en un DataFrame de pandas
            df = pd.read_excel(archivo_entrada)
            print(f"✅ Archivo '{archivo_entrada}' (XLSX) leído con éxito.")
        else:
            print("❌ ERROR: Formato de archivo no soportado. Debe ser '.csv' o '.xlsx'.")
            return
    except Exception as e:
        print(f"❌ ERROR al leer el archivo: {e}")
        return

    # 3. Convertir el DataFrame a JSON y escribirlo
    try:
        # Usar el método to_json() de pandas para la conversión.
        # 'orient="records"' es el formato más común: una lista de diccionarios, 
        # donde cada diccionario es una fila del archivo original.
        df.to_json(archivo_salida, orient="records", indent=4)
        print(f"✅ Conversión a '{archivo_salida}' (JSON) completada.")
        
    except Exception as e:
        print(f"❌ ERROR al escribir el archivo JSON: {e}")
        return

    print("¡Proceso finalizado!")

# --- Ejemplo de Uso ---
"""
# Configuración para un archivo CSV
ARCHIVO_CSV = 'datos_ejemplo.csv'
SALIDA_JSON_CSV = 'datos_ejemplo_csv.json'
"""
# Configuración para un archivo XLSX
ARCHIVO_XLSX = 'data/Texto_base/DatasetLimpio3.xlsx'
SALIDA_JSON_XLSX = 'data/Texto_filtro1/datos3.json'

# Correr el proceso para el CSV
"""
print("--- Procesando CSV ---")
convertir_a_json(ARCHIVO_CSV, SALIDA_JSON_CSV)
"""

# ---
# Correr el proceso para el XLSX
print("\n--- Procesando XLSX ---")
convertir_a_json(ARCHIVO_XLSX, SALIDA_JSON_XLSX)