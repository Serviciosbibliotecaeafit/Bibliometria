# Bibliometria

Recolección, normalización y unificación de datos bibliográficos usando un bot para web scraping.

**Table of Contents**

- [Bibliometria](#bibliometria)
  - [Descripciones](#descripciones)
  - [Librerias](#librerias)
  - [Funcionamiento](#funcionamiento)
  - [Uso](#uso)
  - [Futuro](#futuro)

## Descripciones

---


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

## Librerias

---

- **Pandas** (1.5.3)
- **Selenium** (4.8.2)
- **Webdriver-manager** (3.8.5)
- **JSON**
- **Openpyxl** (3.1.2)
- **PyQt6** (6.5.1)
- **Pyinstaller** (5.11.0)

## Funcionamiento

---

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

---

Actualmente el programa se usa a través del [script `main.py`](#descripciones), por lo que es necesario crear o mover un archivo `.txt` a la carpeta del programa. Para testeo, en la carpeta se puede encontrar con el archivo `test_urls.txt` (252 links) y `test_urls_short.txt` (100 links). De esta forma, para obtener los datos de estos links se usa el comando:

      python main.py [Nombre_del_archivo]

Por ejemplo, para `test_urls.txt` se usa:

      python main.py test_urls


## Futuro

---

- Diseño y creación de una interfaz de usuario gráfica como aplicación de escritorio, se propone usar [`Electronjs`](https://www.electronjs.org/es/) para esto.
