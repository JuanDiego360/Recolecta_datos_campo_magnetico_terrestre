#!/bin/bash

# Directorio del proyecto
PROYECTO_DIR="/home/juandiego/Documentos/proyecto_datos_campo_magnetico"

# Función para mostrar mensajes con formato
mostrar_mensaje() {
    echo -e "\n[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Cambiar al directorio del proyecto
cd "$PROYECTO_DIR" || {
    mostrar_mensaje "Error: No se pudo acceder al directorio $PROYECTO_DIR"
    exit 1
}

# Verificar si hay cambios para subir
mostrar_mensaje "Verificando cambios en el repositorio..."
git_status=$(git status --porcelain)

if [ -z "$git_status" ]; then
    mostrar_mensaje "No hay cambios para subir al repositorio."
    exit 0
fi

# Hay cambios, procedemos con el proceso de subida
mostrar_mensaje "Se encontraron cambios. Iniciando proceso de subida..."

# Añadir todos los cambios
mostrar_mensaje "Añadiendo archivos..."
git add .

# Crear commit
mostrar_mensaje "Creando commit..."
git commit -m "Subir datos nuevos"

# Obtener el token de GitHub
xsel --clipboard < /home/juandiego/token_github.txt

# Subir cambios
mostrar_mensaje "Subiendo cambios al repositorio..."
if git push -u origin main; then
    mostrar_mensaje "¡Los cambios se subieron exitosamente!"
else
    mostrar_mensaje "Error: No se pudieron subir los cambios"
fi

exit 0

