#!/bin/bash

# Directorio base (se obtiene la ruta actual automáticamente)
directorio_base=$(pwd)

# Directorio destino principal
directorio_destino="/home/juandiego/Documentos/proyecto_datos_campo_magnetico"

declare -a ano=()
declare -a numero=()

# Bucle para cada archivo CSV
for archivo in "$directorio_base"/*.csv; do
    # Validamos si el nombre del archivo tiene el formato correcto
    if [[ "$archivo" =~ CampoMagnetico_[0-9]{4}_[0-9]{2}.csv ]]; then
        # Extraemos el año y el número del nombre del archivo
        ano+=($(echo "$archivo" | cut -d'_' -f4))
        numero+=($(echo "$archivo" | cut -d'_' -f5 | sed "s/\.csv//"))
    fi
done

# Convertimos los arrays a formato JSON para pasarlos a Python
anos_json=$(printf '%s\n' "${ano[@]}" | jq -R . | jq -s .)
numeros_json=$(printf '%s\n' "${numero[@]}" | jq -R . | jq -s .)

# Llamamos al script Python y guardamos la salida
python3 verificar_datos.py "$anos_json" "$numeros_json"

# Procesamos los archivos que necesitan ser reemplazados
archivos_corregidos=false
for archivo in "$directorio_base"/*_sinduplicado.csv; do
    if [ -f "$archivo" ]; then
        # Obtenemos el nombre del archivo original
        archivo_original=$(echo "$archivo" | sed 's/_sinduplicado//')
        
        # Eliminamos el archivo original
        rm "$archivo_original"
        
        # Renombramos el archivo sin duplicados
        mv "$archivo" "$archivo_original"
        
        echo "Archivo reemplazado: $archivo_original"
        archivos_corregidos=true
    fi
done

# Volvemos a verificar los archivos corregidos
echo -e "\nVerificando archivos corregidos..."
resultado_verificacion=$(python3 verificar_datos.py "$anos_json" "$numeros_json")

# Si la verificación indica que los errores fueron subsanados, ejecutamos saca_datos.sh
if echo "$resultado_verificacion" | grep -q "fue subsanado exitosamente"; then
    echo -e "\nEjecutando script de movimiento de archivos..."
    ./saca_datos.sh
elif [ "$archivos_corregidos" = false ]; then
    echo "No hubo archivos que necesitaran corrección."
    echo -e "\nEjecutando script de movimiento de archivos..."
    ./sacar_datos.sh
else
    echo "Algunos errores no pudieron ser subsanados. No se moverán los archivos."
fi
