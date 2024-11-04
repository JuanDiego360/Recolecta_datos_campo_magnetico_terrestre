import pandas as pd
import requests
import time
import os
from datetime import datetime

df_gravedad=pd.read_csv("datos_gravedad04.csv")

# Verificamos si ya existe el archivo de resultados
archivo_resultados = 'CampoMagnetico_1965_04.csv'
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
  """Función para guardar los resultados en el archivo CSV"""
  df_nuevo = pd.DataFrame(resultados, columns=['Latitude', 'Longitude', 'MagneticField(nT)'])
  
  if os.path.exists(archivo_resultados):
      # Si el archivo existe, agregamos los nuevos datos sin el encabezado
      df_nuevo.to_csv(archivo_resultados, mode='a', header=False, index=False)
  else:
      # Si es la primera vez, creamos el archivo con encabezado
      df_nuevo.to_csv(archivo_resultados, index=False)

def guardar_errores(coordenadas_error):
  """Función para guardar las coordenadas con error"""
  df_errores = pd.DataFrame(coordenadas_error, columns=['Latitude', 'Longitude', 'Height'])
  df_errores.to_csv(archivo_errores, index=False)

def procesar_coordenada(lat, lon, height, intentos=3):
  """Función para procesar una coordenada y obtener el campo magnético con reintentos"""
  for intento in range(intentos):
      try:
          params = {
              'key': 'EAU2y',
              'lat1': float(lat),
              'lon1': float(lon),
              'elevation': float(height)/1000,
              'elevationUnits': 'K',
              'model': 'IGRF',
              'startYear': 1965,
              'endYear': 1965,
              'resultFormat': 'csv'
          }
          
          response = requests.get(base_url, params=params)
          
          if response.status_code == 200:
              lines = response.text.split('\n')
              for line in lines:
                  if line.startswith('1965'):
                      valores = line.split(',')
                      if len(valores) >= 5:
                          try:
                              return float(valores[4])  # Total Intensity
                          except ValueError:
                              continue
              
              # Si llegamos aquí, no encontramos un valor válido
              if intento < intentos - 1:
                  time.sleep(5)  # Esperar antes de reintentar
                  continue
                  
          elif response.status_code == 429:  # Too Many Requests
              time.sleep(10)
              continue
              
      except Exception as e:
          if intento < intentos - 1:
              time.sleep(5)
              continue
          
  return None

def procesar_errores():
  """Función para procesar las coordenadas que fallaron"""
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
  
  # Guardar resultados restantes
  if nuevos_resultados:
      guardar_resultados(nuevos_resultados)
  
  # Actualizar archivo de errores con las coordenadas que siguen sin resolver
  if coordenadas_sin_resolver:
      guardar_errores(coordenadas_sin_resolver)
  else:
      # Si no hay errores pendientes, eliminar el archivo
      os.remove(archivo_errores)

# Proceso principal
contador = 0
errores = 0

try:
  # Primero procesamos los errores pendientes si existen
  if os.path.exists(archivo_errores):
      procesar_errores()
  
  # Procesamos las coordenadas nuevas
  for index, row in df_gravedad.iterrows():
      lat = float(row['Latitude'])
      lon = float(row['Longitude'])
      
      # Verificamos si ya procesamos esta coordenada
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
      
      # Guardamos cada 40 registros exitosos
      if len(resultados_temp) >= 40:
          guardar_resultados(resultados_temp)
          print(f"Guardados {contador} registros. Último procesado: Lat {lat}, Lon {lon}")
          resultados_temp = []
          time.sleep(1)
      
      # Si acumulamos varios errores, los guardamos
      if len(coordenadas_error) >= 10:
          guardar_errores(coordenadas_error)
          coordenadas_error = []
          
except KeyboardInterrupt:
  print("\nProceso interrumpido por el usuario")
  # Guardamos los datos pendientes antes de salir
  if resultados_temp:
      guardar_resultados(resultados_temp)
  if coordenadas_error:
      guardar_errores(coordenadas_error)
finally:
  # Guardamos cualquier resultado pendiente
  if resultados_temp:
      guardar_resultados(resultados_temp)
  if coordenadas_error:
      guardar_errores(coordenadas_error)
      
print(f"Proceso completado. Total de registros procesados: {contador}")
if os.path.exists(archivo_errores):
  df_errores = pd.read_csv(archivo_errores)
  print(f"Coordenadas con error pendientes: {len(df_errores)}")

# Created/Modified files during execution:
print("CampoMagnetico.csv")
print("coordenadas_error.csv")
