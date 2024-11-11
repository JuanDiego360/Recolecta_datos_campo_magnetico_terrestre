import pandas as pd
import sys
import json
import os

def verificar_completitud(fecha, Num, dire):
  if(dire):
      nombre_data=f"/home/Juandiego/Documentos/proyecto_datos_campo_magnetico/datos_campo_magnetico_{fecha}/data{Num}/CampoMagnetico_{fecha}_{Num}.csv"
  else:
      nombre_data=f"CampoMagnetico_{fecha}_{Num}.csv"
  
  data=pd.read_csv(nombre_data)
  
  if Num in ["01", "02", "03"]:
      if(data.isnull().sum().iloc[2]==0 and len(data)==16335):
          return True
      else:
          print(f"datos incompletos, hacen falta {data.isnull().sum().iloc[2]+16335-len(data)} datos.")
          return False
  elif Num=="04":
      if(data.isnull().sum().iloc[2]==0 and len(data)==16336):
          return True
      else:
          print(f"datos incompletos, hacen falta {data.isnull().sum().iloc[2]+16336-len(data)} datos.")
          return False

def borrar_datos(fecha, Num):
  try:
      # Cargar el dataset
      df = pd.read_csv(f"CampoMagnetico_{fecha}_{Num}.csv")

      # Identificar y eliminar duplicados considerando solo latitud y longitud
      df = df.drop_duplicates(subset=['Latitude', 'Longitude'])

      # Guardar el nuevo DataFrame
      df.to_csv(f"CampoMagnetico_{fecha}_{Num}_sinduplicado.csv", index=False)

      print(f"Se han eliminado los duplicados del archivo CampoMagnetico_{fecha}_{Num}.csv")
      return True
  except Exception as e:
      print(f"Error al procesar el archivo: {e}")
      return False

# Recibimos los argumentos JSON y los convertimos a listas
fecha = json.loads(sys.argv[1])
Num = json.loads(sys.argv[2])

# Asumimos que los archivos están en el directorio actual
fuera = False

# Diccionario para almacenar los archivos con error
archivos_con_error = {}

for i, j in zip(fecha, Num):
  resultado = True
  resultado = resultado and verificar_completitud(i, j, fuera)
  if(not resultado):
      print(f"El data incompleto es el data_{j} del año {i}")
      # Si el resultado es falso, ejecutamos la función borrar_datos
      print(f"Intentando corregir archivo del año {i}, número {j}")
      if borrar_datos(i, j):
          archivos_con_error[f"{i}_{j}"] = True
      else:
          archivos_con_error[f"{i}_{j}"] = False
  else:
      print(f"data_{j} del año {i} completo")

# Verificar si estamos en la segunda ejecución (verificación post-corrección)
if os.path.exists("verificacion_anterior.txt"):
  # Leer los resultados anteriores
  with open("verificacion_anterior.txt", "r") as f:
      archivos_anteriores = json.load(f)
  
  # Comparar resultados
  for archivo in archivos_con_error:
      if archivo in archivos_anteriores:
          if not archivos_con_error[archivo]:
              print(f"\nNo se pudo solucionar el error en el archivo {archivo}")
          else:
              print(f"\nEl error en el archivo {archivo} fue subsanado exitosamente")
  
  # Eliminar el archivo temporal
  os.remove("verificacion_anterior.txt")
else:
  # Guardar los resultados de la primera verificación
  with open("verificacion_anterior.txt", "w") as f:
      json.dump(archivos_con_error, f)
