import pandas as pd

# Suponiendo que ya tienes tu DataFrame df_gravedad cargado
df_gravedad=pd.read_csv("CampoMagnetico_sinduplicado.csv")

# Número de filas por partición (excepto la última)
filas_por_particion = 16335

# Calculando los índices donde se harán los cortes
indices_corte = [filas_por_particion, filas_por_particion * 2, filas_por_particion * 3]

# Dividiendo el DataFrame y guardando cada partición en un CSV
for i in range(4):
    if i < 3:
        inicio = i * filas_por_particion
        fin = (i + 1) * filas_por_particion
    else:
        inicio = indices_corte[2]
        fin = len(df_gravedad)
    
    df_particion = df_gravedad.iloc[inicio:fin]
    nombre_archivo = f"CampoMagnetico_2011_{i+1:02d}.csv"
    df_particion.to_csv(nombre_archivo, index=False)
