#!/bin/bash
Num=0
Num_sobrescritos=0
Num_omitidos=0

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
    archivo_destino="$directorio_final/$(basename "$archivo")"

    # Verificamos si el archivo ya existe en el destino
    if [ -f "$archivo_destino" ]; then
      echo "El archivo $(basename "$archivo") ya existe en el destino."
      
      # Comparamos los archivos para ver si son diferentes
      if cmp -s "$archivo" "$archivo_destino"; then
        echo "Los archivos son idénticos. Omitiendo..."
        ((Num_omitidos=Num_omitidos+1))
      else
        echo "Los archivos son diferentes."
        read -p "¿Desea sobrescribir el archivo existente? (s/n): " respuesta
        if [[ $respuesta =~ ^[Ss]$ ]]; then
          mv -f "$archivo" "$archivo_destino"
          echo "Archivo sobrescrito."
          ((Num_sobrescritos=Num_sobrescritos+1))
          ((Num=Num+1))
        else
          echo "Operación cancelada para este archivo."
          ((Num_omitidos=Num_omitidos+1))
        fi
      fi
    else
      # Si el archivo no existe, simplemente lo movemos
      mv "$archivo" "$directorio_final"
      ((Num=Num+1))
    fi
  fi
done

echo "Resumen de operaciones:"
echo "$Num archivos movidos en total"
echo "$Num_sobrescritos archivos sobrescritos"
echo "$Num_omitidos archivos omitidos"

