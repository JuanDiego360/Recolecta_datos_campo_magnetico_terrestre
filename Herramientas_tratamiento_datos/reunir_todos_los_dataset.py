import pandas as pd

# Lista con los nombres de los archivos CSV
archivos_csv = [f"datos_gravedad{i+1:02d}.csv" for i in range(4)]

# Crear una lista vacía para almacenar los DataFrames
dataframes = []

# Leer cada archivo CSV y agregar el DataFrame a la lista
for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    dataframes.append(df)

# Concatenar todos los DataFrames en uno solo
df_completo = pd.concat(dataframes, ignore_index=True)

# Guardar el DataFrame resultante en un nuevo archivo CSV (opcional)
df_completo.to_csv("datos_gravedad_completo.csv", index=False)
