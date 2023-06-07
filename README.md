# Bibliometria

Versión: 0.1.0

****

Recolección, normalización y unificación de datos bibliográficos usando un bot para web scraping.

**Table of Contents**

- [Bibliometria](#bibliometria)
  - [Descripciones](#descripciones)
  - [Librerias](#librerias)
  - [Funcionamiento](#funcionamiento)
  - [Uso](#uso)
    - [Instalación](#instalación)
    - [Manejo](#manejo)

## Descripciones

****

- **`selenium_outputs/BACKUP.csv`:** Archivo de respaldo donde se guardan los últimos datos recolectados por el bot en caso de un paro total.
- **`selenium_outputs/log.out`:** Archivo de registro del proceso de web scraping donde se muestra el registro de respaldos y de errores presentados.
- **`UI/main.qml`:** Archivo principal de la interfaz gráfica.
- **`main.py`:** Script de ejecución principal encargado de conectar la aplicación de escritorio con los scripts de python.
- **`main.spec`:** Archivo de configuración para la construcción de la aplicación mediante pyInstaller.
- **`main_program.py`:** Script con las funciones y algoritmos para llamar los procedimientos de obtención y normalización de datos, además de los procesos de exportación de los datos.
- **`selenium_methods.py`:** Script con las funciones y algoritmos generales para realizar web scraping mediante la libreria Selenium.
- **`norm_methods.py`:** Script con las funciones y algoritmos para normalizar los datos obtenidos mediante web-scraping.
- **`selenium_conf.json`:** Archivo con los datos de logeo y direcciones Xpaths para la extracción de la información.
- **`installforgeSttings.ifp`:** Archivo de configuración para crear el instalador mediante InstallForge.
- **`test_urls.txt`:** Archivo input de ejemplo para testeo del programa.
- **`Data.xlsx`:** Archivo de excel con los datos de salida normalizados.
- **`output.csv`:** Archivo en formato csv con los datos de salida normalizados.
- **`outputRAW.csv`:** Archivo en formato csv con los datos de salida sin normalizar.
- **`ìnstallationTest/installBibliometria.exe`:** Instalador del programa

## Librerias

****

- **Pandas** (1.5.3)
- **Selenium** (4.8.2)
- **Webdriver-manager** (3.8.5)
- **JSON**
- **Openpyxl** (3.1.2)
- **PyQt6** (6.5.1)
- **Pyinstaller** (5.11.0)

## Funcionamiento

****

Ahora el proceso parte de una lista de URLs de donde se desean obtener los datos bibliográficos para lo cual se introducen al bot de Selenium. Para tener una obtención de datos adecuadas se debe realizar un pre-registro de la base de datos (página web) de donde se desea obtener la info, en el momento solo se tiene registrada la base de SCOPUS.

El proceso para realizar el preregistro es el siguiente:

1. Crear un archivo `.json` usando como plantilla el existente para la base de datos SCOPUS
2. Introducir credenciales de logeo para la página web (en caso de que sea necesario) así como el link directo a la página de logeo.
3. Crear un diccionario de XPath's para cada dato que se desea encontrar, se organiza en formato de array ya que pueden haber múltiples XPath's para un solo dato, por lo que se organiza en el array de tal forma que el primer XPath sea el más común. Para encontrar un XPath realize el siguiente proceso:

   3.1. Dirigase a la página web de donde desea obtener el dato

   3.2 De click derecho al dato que desea extraer y seleccione `Inspeccionar`, se le abrirán las herramientas de desarrollador con el archivo `.html` de la web.

   3.3 Repita el proceso para asegurarse que esté en el lugar correcto del archivo `.html` donde se encuentra el dato.

   3.4 Navegue por el archivo `.html` cerca de la posición en la que se le abrió, verá que varias zonas de la página se le resaltarán al pasar el mouse
   por el archivo `.html`.

   3.5 Cuando tenga resaltada la zona correspondiente a su dato o encontró el dato específico en el código, seleccione con el mouse la zona del código o el dato en el código, en las opciones que le aparecieron ponga el mouse sobre la opción `Copiar`, en las nuevas opciones de click donde dice `Copiar XPath Completo` o `Copy Full XPath`.

En el archivo `.json` se puede observar un XPath auxiliar que se puede usar para realizar ubicaciones relativas de algunos datos en la página web, esto puede llegar a ser muy especializado para cada base de datos por lo que habría que acondicionar el proceso realizado por Selenium en comparación al que se realiza actualmente para SCOPUS.

## Uso

****

### Instalación

Para instalar la aplicación descargue el [instalador](installationTest/installBibliometria.exe) y siga las instrucciones. También, tenga en cuenta tener instalado en su computador el navegador **Google Chrome**.

### Manejo

Los pasos a seguir son:

- **Introduzca Base de Datos:** De click en seleccionar y se desplegará una lista con las bases de datos registradas en la versión actual de la aplicación, seleccione la correspondiente a los links de donde desea obtener los datos.
- **Introduzca el Archivo de Entradas:** De click en seleccionar, se le abrirá un buscador donde deberá seleccionar el archivo `.txt` conteniendo los links.
- **Introduzca Credenciales:** Introduzca su correo y contraseña que usa para acceder a la base de datos seleccionada.
- **Introduzca Carpeta de Salida:** De click en seleccionar, se le abrirá un buscador donde deberá dirigirse a la carpeta donde desea guardar los datos.

Una vez introducidos todos los datos, podrá dar click a `Obtener Datos`. A continuación, se le abrirá una terminal y un navegador de Google Chrome para dar inicio a la obtención de datos y en el panel derecho observará que el registro de obtención. El avance del proceso lo podrá observar a través de la barra de progreso justo debajo de `Obtener Datos`.

Cuando se de por terminado la obtención de datos, observará la barra de progreso a desaparecido y ahora encontrará un boton con el texto `Exportar`, al darle click los datos obtenidos serán exportados en formato `.csv` y `.xlsx` en la carpeta que usted halla seleccionado.

**Advertencia:** Si observa que el navegador se cerró, la barra de progreso no a desparecido y el registro no menciona el fin de registro, entonces algún error ocurrió en la obtención de los datos. Por lo que tienes una de las siguientes dos opciones:

- Reiniciar el programa y volver a iniciar la obtención de datos.
- Dar click en `Exportar Backup`, con lo que se exportarán los datos obtenidos hasta donde logró el programa, siendo el último registro el mencionado en el panel derecho. Luego, reinicie el programa e introduzca los links que faltaron anteriormente. **Nota:** Tenga en cuenta que el backup se exportará con el nombre `Data.*`, por lo que si no cambia el nombre manualmente antes de que el programa termine de correr por segunda vez, los datos se sobreescribiran.
