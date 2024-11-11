#!/bin/bash

# Directorio base
BASE_DIR="/home/juandiego/Documentos/proyecto_datos_campo_magnetico"

# Cambiar al directorio base
cd "$BASE_DIR" || {
    echo "Error: No se puede acceder al directorio $BASE_DIR"
    exit 1
}

# Función para verificar archivo
verificar_archivo() {
    local dir=$1
    local ano=$2
    local num=$3
    local archivo="CampoMagnetico_${ano}_${num}.csv"
    
    if [ -f "$dir/$archivo" ]; then
        echo "    Encontrado: $archivo"
        return 0
    else
        echo "    No encontrado: $archivo"
        return 1
    fi
}

# Función para procesar un año
procesar_ano() {
    local ano="$1"
    local dir_ano="datos_campo_magnetico_${ano}"
    
    # Verificar si el directorio existe
    if [ ! -d "$dir_ano" ]; then
        echo "El directorio $dir_ano no existe"
        return
    fi

    echo "Procesando año $ano en $dir_ano"
    
    # Verificar subdirectorios y archivos
    local archivos_completos=true
    
    for num in {1..4}; do
        local num_pad=$(printf "%02d" $num)
        local data_dir="$dir_ano/data$num_pad"
        
        echo "  Verificando directorio: $data_dir"
        
        if [ ! -d "$data_dir" ]; then
            echo "  ✗ Directorio data$num_pad no existe"
            archivos_completos=false
            break
        fi
        
        if ! verificar_archivo "$data_dir" "$ano" "$num_pad"; then
            archivos_completos=false
            break
        fi
    done
    
    # Si todos los archivos están presentes, procesar con Python
    if [ "$archivos_completos" = true ]; then
        echo "  Todos los archivos encontrados para $ano, procesando..."
        
        # Crear script Python temporal
        cat > temp_script.py << EOF
import pandas as pd
import os

try:
    # Lista de archivos CSV
    dataframes = []
    
    # Leer cada archivo CSV
    for i in range(4):
        num = f"{i+1:02d}"
        archivo = f"$dir_ano/data{num}/CampoMagnetico_${ano}_{num}.csv"
        print(f"Leyendo archivo: {archivo}")
        if os.path.exists(archivo):
            df = pd.read_csv(archivo)
            dataframes.append(df)
        else:
            print(f"Archivo no encontrado: {archivo}")
            exit(1)

    # Concatenar todos los DataFrames
    df_completo = pd.concat(dataframes, ignore_index=True)
    
    # Guardar el resultado
    output_file = "$dir_ano/CampoMagnetico_${ano}.csv"
    df_completo.to_csv(output_file, index=False)
    print(f"Archivo creado exitosamente: {output_file}")
    
except Exception as e:
    print(f"Error: {str(e)}")
    exit(1)
EOF

        echo "  Ejecutando script Python..."
        if python3 temp_script.py; then
            echo "  ✓ Archivo CampoMagnetico_${ano}.csv creado exitosamente"
        else
            echo "  ✗ Error al procesar los datos del año $ano"
        fi
        
        # Limpiar archivo temporal
        rm temp_script.py
    else
        echo "  ✗ No se encontraron todos los archivos necesarios para $ano"
    fi
    
    echo "----------------------------------------"
}

# Listar todos los directorios para verificar
echo "Directorios encontrados:"
ls -d datos_campo_magnetico_* 2>/dev/null

# Procesar cada año
echo "Iniciando procesamiento de datos magnéticos..."
for year in {1965..2016}; do
    procesar_ano "$year"
done

echo "Proceso completado"
