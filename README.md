# Bibliometria

Recolección, normalización y unificación de datos bibliográficos usando un bot para web scraping.

**Nota**: Aquellas librerias, carpetas, archivos, etc. que estén marcados como **(NO EN USO)**, se refiere a que no son usados actualmente en la ejecución del programa pero están disponible para su manipulación en el desarrollo.

**Table of Contents**

- [Bibliometria](#bibliometria)
  - [Descripciones](#descripciones)
  - [Librerias](#librerias)
  - [Funcionamiento](#funcionamiento)
  - [Instalación en Windows](#instalación-en-windows)
    - [*Instalación de Python y Ambiente Virtual*](#instalación-de-python-y-ambiente-virtual)
    - [*Descarga*](#descarga)
      - [*Clonación del Repositorio*](#clonación-del-repositorio)
      - [*Descarga Directa*](#descarga-directa)
    - [*Instalación de Librerias*](#instalación-de-librerias)
    - [*Acceso*](#acceso)
  - [Uso](#uso)
  - [Futuro](#futuro)

## Descripciones

---

- **`{NOMBRE_BASE}/`(NO EN USO):** Carpeta con los datos sin unificar correspondientes a una base bibliográfica específica con nombre {NOMBRE_BASE}, e.g. LENS, SCIELO, WOS, etc.
- **`Unificar_Data_{NOMBRE_BASE}.ipynb`(NO EN USO):** Notebook donde se realiza la unificación de los datos de una base espécifica con nombre {NOMBRE_BASE}.
- **`Unificar_Data.ipynb`(NO EN USO):** Notebook donde se ejecutan las funciones y algoritmos que unifican globalmente y normalizan los datos de todas las bases bibliográficas.
- **`main.py`:** Script de ejecución principal encargado de leer un `.txt` con las urls, también ejecuta la función principal para obtener los datos y exporta lo obtenido a formato excel.
- **`utilities.py`(NO EN USO):** Script con las funciones y algoritmos necesarios para la unificación y normalización de los datos.
- **`selenium_methods.py`:** Script con las funciones y algoritmos generales para realizar web scraping mediante la libreria Selenium.
- **`selenium_conf.json`:** Archivo con los datos de logeo y direcciones Xpaths para la extracción de la información.
- **`BACKUP.csv`:** Archivo de respaldo donde se guardan los últimos datos recolectados por el bot en caso de un paro total.
- **`log.out`:** Archivo de registro del proceso de web scraping donde se muestra el registro de respaldos y de errores presentados.

## Librerias

---

- **Pandas** (1.5.3)
- **Numpy (NO EN USO)** (1.24.2)
- **Nameparser (NO EN USO)** (1.1.2)
- **Selenium** (4.8.2)
- **Webdriver-manager** (3.8.5)
- **JSON**
- **TQDM** (4.65.0)

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

## Instalación en Windows

---

Este es un pequeño tutorial de todo lo necesario para usar el programa en su versión actual.

### *Instalación de Python y Ambiente Virtual*

Debido que hasta el momento no existe una interfáz de usuario gráfica, se recomienda trabajar desde un ambiente virtual, para lo cual recomendamos usar [Anaconda](https://www.anaconda.com/download#downloads) como un todo en uno.

Una vez instalado Anaconda buscamos en la barra de tareas `Anaconda Prompt` y abrimos la aplicación. En esta terminal [crearemos el ambiente virtual](https://medium.com/co-learning-lounge/create-virtual-environment-python-windows-2021-d947c3a3ca78) mediante la introducción de comandos. Primero nos aseguramos de tener instalado `Conda` para lo cual ingresamos:

      conda -V

Y verificamos que esté actualizado:

      conda update conda

Ahora creamos el ambiente virtual:

      conda create --name Bibliometria python=3.10.6

Aquí se introduce `python=3.10.6` ya que es la versión en la que se ha trabajado hasta ahora el desarrollo.

Una vez creado el ambiente virtual podemos ingresar a este mediante el comando:

      conda activate Bibliometria

O directamente desde la barra de tareas buscando `Anaconda Prompt` y seleccionando aquel denotado por `(Bibliometria)`.

### *Descarga*

En este momento hay dos opciones para descargar el programa: Clonación del repositorio o Descarga directa del repositorio. La primera opción es ideal para aportar al desarrollo del programa y mantener actualización constante a través de GitHub, la segunda es mejor para su uso directo.

#### *Clonación del Repositorio*

Para esta opción es necesario instalar la aplicación de [`GitHub Desktop`](https://desktop.github.com/) (si se tiene conocimientos en el uso de `Git` este programa no es necesario). Es recomendable leer la [documentación](https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/overview/getting-started-with-github-desktop) si se tiene problemas con el ingreso de la cuenta de GitHub al programa de escritorio.

Una vez se tenga `GitHub Desktop` instalado y configurado se debe [clonar el repositorio](https://docs.github.com/es/desktop/contributing-and-collaborating-using-github-desktop/adding-and-cloning-repositories/cloning-a-repository-from-github-to-github-desktop).

#### *Descarga Directa*

Nos dirigimos a la página del [repositorio en GitHub](https://github.com/Serviciosbibliotecaeafit/Bibliometria) y damos click izquierdo en el botón verde `< > Code`. En la pestaña que se nos abre damos click izquierdo en `Download ZIP` y se nos comenzará a descargar el archivo comprimido.

Una vez descargado el `.ZIP`, lo descomprimimos y la carpeta generada la movemos a un lugar de fácil acceso.

### *Instalación de Librerias*

Para que el programa funcione adecuadamente se debe ejecutar el siguiente comando en la terminal de Anaconda (estando en el ambiente virtual `Bibliometria`):

      pip install pandas==1.5.3 selenium==4.8.2 tqdm==4.65.0 webdriver-manager==3.8.5

Si se obtiene algún error, entonces instalar cada libreria por separado, por ejemplo:

      pip install selenium==4.8.2

### *Acceso*

Finalmente tenemos descargado el programa y listo para su uso a través de la terminal de Anaconda. Para usar el programa debemos movernos a la carpeta dónde guardamos el repositorio/programa y copiar la dirección de esta (doble click en la barra superior de navegación, click derecho y damos click izquierdo en copiar). Ahora, en la terminal de Anaconda nos debe aparecer `(Bibliometria)` (esto quiere decir que estamos en el ambiente virtual adecuado), aquí introducimos el siguiente comando para dirigirnos a la carpeta del repositorio:

      cd [dirección del repositorio]

Por ejemplo, si el programa se encuentra en `C:\Users\user\Documentos\GitHub\Bibliometria`:

      cd C:\Users\user\Documentos\GitHub\Bibliometria

Así nos encontramos en la carpeta del repositorio listos para usar el programa.

## Uso

---

Actualmente el programa se usa a través del [script `main.py`](#descripciones), por lo que es necesario crear o mover un archivo `.txt` a la carpeta del programa e modificar en el script `main.py` la variable `url_file_name` con el nombre del nuevo archivo. Para testeo, en el script se puede encontrar el nombre `"test_urls"` referentes al archivo `test_urls.txt` que se encuentra en la carpeta.


## Futuro

---

- Diseño y creación de una interfaz de usuario gráfica como aplicación de escritorio, se propone usar [`Electronjs`](https://www.electronjs.org/es/) para esto.