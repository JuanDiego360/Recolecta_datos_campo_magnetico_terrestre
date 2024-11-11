#!/bin/bash
Num=0
# Directorio base (se obtiene la ruta actual automáticamente)
directorio_base=$(pwd)

# Directorio destino principal
directorio_destino="/home/juandiego/Documentos/proyecto_datos_campo_magnetico"

# Bucle para cada archivo CSV
for archivo in "$directorio_base"/*.csv; do
  # Validamos si el nombre del archivo tiene el formato correcto
  if [[ "$archivo" =~ CampoMagnetico_[0-9]{4}_[0-9]{2}.csv ]]; then
    # Extraemos el año y el número del nombre del archivo
    ano=$(echo "$archivo" | cut -d'_' -f4)
    numero=$(echo "$archivo" | cut -d'_' -f5 | sed "s/\.csv//")

    # Construimos la ruta del directorio destino
    directorio_final="$directorio_destino/datos_campo_magnetico_$ano/data$numero"
    #echo "$directorio_final"

    # Creamos el directorio si no existe
    #mkdir -p "$directorio_final"

    # Movemos el archivo al directorio destino
    mv "$archivo" "$directorio_final"
    ((Num=Num+1))
  fi
done
echo "$Num archivos movidos"
