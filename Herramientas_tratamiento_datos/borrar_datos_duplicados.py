import pandas as pd

# Cargar el dataset
df = pd.read_csv("CampoMagnetico.csv")  # Reemplaza "tu_archivo.csv" con el nombre de tu archivo

# Identificar y eliminar duplicados considerando solo latitud y longitud
df = df.drop_duplicates(subset=['Latitude', 'Longitude'])

# Guardar el nuevo DataFrame
df.to_csv("CampoMagnetico_sinduplicado.csv", index=False)

print("Se han eliminado los duplicados y el nuevo archivo se ha guardado.")
