
# Bienvenido al proyecto de recopilación de datos del campo magnético de la Tierra (1965-2016)

Este proyecto se centra en la recopilación de datos del campo magnético terrestre con ayuda de una API de la NOAA (Administración Nacional Oceánica y Atmosférica). Puede acceder a la base de datos donde se recopilan los datos [aquí](https://data.aad.gov.au/metadata/records/AAS_4092_Geomagnetic_Field_Model).

## Instrucciones

Para colaborar en este proyecto, es importante tener en cuenta que puede utilizar tanto el celular como la computadora. Es necesario tener instalado Python en su dispositivo y contar con la librería `pandas`, ya que esta biblioteca facilita el tratamiento adecuado de los datos recopilados.

Para comenzar a contribuir al proyecto, siga estos pasos:

1. Abra una de las carpetas que se encuentran en la parte superior de esta página. El nombre de cada carpeta tiene el formato `datos_campo_magnetico_{año}`, donde `{año}` representa el año para el cual se van a recopilar los datos.

2. Dentro de cualquiera de esas carpetas encontrará otras subcarpetas llamadas `data01`, `data02`, `data03` y `data04`. La razón por la cual hay cuatro carpetas es para dividir los datos en partes más pequeñas y facilitar su recopilación. Elija cualquiera de esas carpetas y ábrala.

3. En esa carpeta encontrará dos archivos (si aún no se han procesado los datos para esa fecha; <font color="red">por favor, si encuentra más de dos archivos, busque otro directorio porque ese ya ha sido procesado</font>). Uno es un archivo `.csv` llamado `datos_gravedad{número}.csv`, que contiene las latitudes, longitudes, alturas y datos de gravedad de cada punto de la Tierra desde -180 a 180 grados de longitud y de -90 a 90 grados de latitud, en incrementos de un grado. El otro archivo se llama `obtener_campo_magnetico2.py` y es un script de Python que debe ejecutar para iniciar la recopilación de los datos. Descargue ambos archivos del repositorio de GitHub y guárdelos en una carpeta.

4. Una vez descargados los archivos, ejecute el script de Python. Este script está programado para recopilar los datos del campo magnético en las latitudes y longitudes especificadas en el archivo `datos_gravedad{número}.csv`. Es importante mencionar que el script guarda automáticamente los datos cada 40 registros y también cuenta con un mecanismo para manejar datos defectuosos o errores del servidor, lo cual permite decidir si es necesario recalcular.

5. Al finalizar el proceso, tendrá un archivo llamado `CampoMagnetico_{año}_{número}.csv`, que contiene las mediciones del campo magnético. En caso de que se produzca un error, se generará un archivo llamado `coordenadas_error.csv`, el cual contiene los datos que no se calcularon correctamente (este archivo solo se genera cuando hay errores en la obtención de los datos). Envíe los archivos generados a juandiego212014@gmail.com, incluyendo su nombre para agregarlo como contribuyente a la base de datos.

6. Una vez completados todos los datos, se unirán en una sola matriz tridimensional para facilitar su descarga.

A continuación, se presenta una guía para contribuir desde una PC o un dispositivo Android.

## PC

Para recopilar datos desde una PC, solo necesita tener Python instalado en su máquina. A continuación, se proporcionan enlaces a tutoriales sobre cómo hacerlo en distintos sistemas operativos.

### Windows

- Instalación de Python [aquí](https://www.youtube.com/watch?v=i6j8jT_OdEU)
- Instalación de `pandas` [aquí](https://www.youtube.com/watch?v=SWIIQboGGCQ)

### Ubuntu

- Instalación de Python [aquí](https://www.youtube.com/watch?v=88np4KkfDO8)
- Instalación de `pandas` [aquí](https://www.youtube.com/watch?v=hRCPqE-lSsI)

## Android

Para recopilar datos desde un dispositivo Android, siga estos pasos:

1. Descargue Termux desde F-Droid, disponible [aquí](https://f-droid.org/es/packages/com.termux/).

2. Una vez instalado Termux, abra la aplicación y ejecute los siguientes comandos:
   - `pkg upgrade` (para actualizar los paquetes de Termux)
   - `pkg install python` (para instalar Python en Termux)
   - `pkg install python-numpy` (para instalar `numpy`)
   - `pkg install tur-repo` (para resolver posibles problemas al instalar `pandas`)
   - `pkg install python-pandas` (para instalar `pandas`)
   - `pip list` (para verificar si los paquetes `numpy` y `pandas` se instalaron correctamente)
   - `termux-setup-storage` (para acceder a los archivos del dispositivo desde Termux)
   - `ls` (debería aparecer un directorio llamado `storage`)
   - `cd storage` (para acceder al directorio `storage`)
   - `cd shared` (para acceder al directorio `shared`)
   - `mkdir campo_magnetico` (para crear un directorio llamado `campo_magnetico`)

3. Descargue los archivos en `data01`, `data02`, `data03` y `data04` y colóquelos dentro de ese directorio creado.

4. Regrese a Termux y acceda al directorio `campo_magnetico`, con el comando `cd campo_magnetico`.

5. Ejecute el archivo `obtener_campo_magnetico2.py` con el siguiente comando: `python obtener_campo_magnetico2.py`.

6. Envíe los datos a mi correo electrónico una vez que el proceso haya finalizado.

## Contribuyentes:

- Cristian Vargas (estudiante de física de la Universidad de Pamplona)
