import pandas as pd
import requests
import time
import os
from datetime import datetime

df_gravedad=pd.read_csv("datos_gravedad03.csv")

# Verificamos si ya existe el archivo de resultados
archivo_resultados = 'CampoMagnetico_1977_03.csv'
archivo_errores = 'coordenadas_error.csv'
registros_procesados = set()
coordenadas_error = []

if os.path.exists(archivo_resultados):
    # Leemos los registros ya procesados
    df_existente = pd.read_csv(archivo_resultados)
    # Creamos un conjunto de tuplas (lat, lon) ya procesadas
    registros_procesados = set(zip(df_existente['Latitude'], df_existente['Longitude']))
    print(f"Encontrados {len(registros_procesados)} registros ya procesados")

# URL base de la API
base_url = "https://www.ngdc.noaa.gov/geomag-web/calculators/calculateIgrfwmm"

# Lista temporal para almacenar los resultados
resultados_temp = []

def guardar_resultados(resultados):
    df_nuevo = pd.DataFrame(resultados, columns=['Latitude', 'Longitude', 'MagneticField(nT)'])
    
    if os.path.exists(archivo_resultados):
        df_nuevo.to_csv(archivo_resultados, mode='a', header=False, index=False)
    else:
        df_nuevo.to_csv(archivo_resultados, index=False)

def guardar_errores(coordenadas_error):
    df_errores = pd.DataFrame(coordenadas_error, columns=['Latitude', 'Longitude', 'Height'])
    df_errores.to_csv(archivo_errores, index=False)

def procesar_coordenada(lat, lon, height, intentos=3):
    for intento in range(intentos):
        try:
            params = {
                'key': 'EAU2y',
                'lat1': float(lat),
                'lon1': float(lon),
                'elevation': float(height)/1000,
                'elevationUnits': 'K',
                'model': 'IGRF',
                'startYear': 1977,
                'endYear': 1977,
                'resultFormat': 'csv'
            }
            
            response = requests.get(base_url, params=params)
            
            if response.status_code == 200:
                lines = response.text.split('\n')
                for line in lines:
                    if line.startswith('1977'):
                        valores = line.split(',')
                        if len(valores) >= 5:
                            try:
                                return float(valores[4])
                            except ValueError:
                                continue
                
                if intento < intentos - 1:
                    time.sleep(5)
                    continue
                    
            elif response.status_code == 429:
                time.sleep(10)
                continue
                
        except Exception as e:
            if intento < intentos - 1:
                time.sleep(5)
                continue
            
    return None

def procesar_errores():
    if not os.path.exists(archivo_errores):
        return
        
    print("Procesando coordenadas con errores previos...")
    df_errores = pd.read_csv(archivo_errores)
    nuevos_resultados = []
    coordenadas_sin_resolver = []
    
    for index, row in df_errores.iterrows():
        campo_magnetico = procesar_coordenada(row['Latitude'], row['Longitude'], row['Height'])
        
        if campo_magnetico is not None:
            nuevos_resultados.append({
                'Latitude': row['Latitude'],
                'Longitude': row['Longitude'],
                'MagneticField(nT)': campo_magnetico
            })
            
            if len(nuevos_resultados) >= 40:
                guardar_resultados(nuevos_resultados)
                nuevos_resultados = []
                time.sleep(1)
        else:
            coordenadas_sin_resolver.append({
                'Latitude': row['Latitude'],
                'Longitude': row['Longitude'],
                'Height': row['Height']
            })
    
    if nuevos_resultados:
        guardar_resultados(nuevos_resultados)
    
    if coordenadas_sin_resolver:
        guardar_errores(coordenadas_sin_resolver)
    else:
        os.remove(archivo_errores)

# Proceso principal
contador = 0
errores = 0

try:
    if os.path.exists(archivo_errores):
        procesar_errores()
    
    for index, row in df_gravedad.iterrows():
        lat = float(row['Latitude'])
        lon = float(row['Longitude'])
        
        if (lat, lon) in registros_procesados:
            continue
            
        campo_magnetico = procesar_coordenada(lat, lon, row['Height'])
        
        if campo_magnetico is not None:
            resultados_temp.append({
                'Latitude': lat,
                'Longitude': lon,
                'MagneticField(nT)': campo_magnetico
            })
            contador += 1
        else:
            coordenadas_error.append({
                'Latitude': lat,
                'Longitude': lon,
                'Height': row['Height']
            })
            errores += 1
        
        if len(resultados_temp) >= 40:
            guardar_resultados(resultados_temp)
            print(f"Guardados {contador} registros. Último procesado: Lat {lat}, Lon {lon}")
            resultados_temp = []
            time.sleep(1)
        
        if len(coordenadas_error) >= 10:
            guardar_errores(coordenadas_error)
            coordenadas_error = []
            
except KeyboardInterrupt:
    print("\nProceso interrumpido por el usuario")
    if resultados_temp:
        guardar_resultados(resultados_temp)
    if coordenadas_error:
        guardar_errores(coordenadas_error)
finally:
    if resultados_temp:
        guardar_resultados(resultados_temp)
    if coordenadas_error:
        guardar_errores(coordenadas_error)
        
print(f"Proceso completado. Total de registros procesados: {contador}")
if os.path.exists(archivo_errores):
    df_errores = pd.read_csv(archivo_errores)
    print(f"Coordenadas con error pendientes: {len(df_errores)}")
