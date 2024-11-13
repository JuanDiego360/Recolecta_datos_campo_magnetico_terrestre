#!/bin/bash

rm lista_complete.org

# Directorio base
BASE_DIR="/home/juandiego/Documentos/proyecto_datos_campo_magnetico"
LISTA_FILE="$BASE_DIR/lista_complete.org"

# Función para crear el archivo template si no existe
crear_template() {
    cat > "$LISTA_FILE" << EOF
#+TITLE: Lista de verificación de datos magnéticos por año
#+DATE: $(date '+%Y-%m-%d')

* Años procesados
EOF
    
    # Añadir todos los años
    for ano in {1965..2016}; do
        echo "- [ ] $ano" >> "$LISTA_FILE"
    done
}

# Crear el archivo si no existe
if [ ! -f "$LISTA_FILE" ]; then
    echo "Creando archivo lista_complete.org..."
    crear_template
fi

# Contador para estadísticas
total_completados=0

# Procesar cada año
for ano in {1965..2016}; do
    dir_ano="$BASE_DIR/datos_campo_magnetico_$ano"
    archivo_completo="$dir_ano/CampoMagnetico_$ano.csv"
    
    if [ -f "$archivo_completo" ]; then
        # Marcar como completado
        sed -i "s/- \[ \] $ano/- [X] $ano/" "$LISTA_FILE"
        ((total_completados++))
    else
        # Asegurarse de que está marcado como incompleto
        sed -i "s/- \[X\] $ano/- [ ] $ano/" "$LISTA_FILE"
    fi
done

# Calcular estadísticas
total_anos=$((2016 - 1965 + 1))
porcentaje=$(( (total_completados * 100) / total_anos ))

# Añadir o actualizar estadísticas al final del archivo
if grep -q "* Estadísticas" "$LISTA_FILE"; then
    # Actualizar estadísticas existentes
    sed -i "/\* Estadísticas/,/\* /c\* Estadísticas\n- Años completados: $total_completados de $total_anos\n- Porcentaje completado: $porcentaje%" "$LISTA_FILE"
else
    # Añadir estadísticas nuevas
    cat >> "$LISTA_FILE" << EOF

* Estadísticas
- Años completados: $total_completados de $total_anos
- Porcentaje completado: $porcentaje%
EOF
fi

echo "Lista actualizada exitosamente"
echo "Total años completados: $total_completados de $total_anos ($porcentaje%)"
