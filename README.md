# Bibliometria

Recolección, normalización y unificación de datos bibliográficos usando un bot para web scraping.

---

## Descripciones

- **`{NOMBRE_BASE}/`:** Directorio con los datos sin unificar correspondientes a una base bibliográfica específica con nombre {NOMBRE_BASE}, e.g. LENS, SCIELO, WOS, etc.
- **`Unificar_Data_{NOMBRE_BASE}.ipynb`:** Notebook donde se realiza la unificación de los datos de una base espécifica con nombre {NOMBRE_BASE}.
- **`Unificar_Data.ipynb`:** Notebook donde se ejecutan las funciones y algoritmos que unifican globalmente y normalizan los datos de todas las bases bibliográficas.
- **`utilities.py`(NO EN USO):** Script con las funciones y algoritmos necesarios para la unificación y normalización de los datos.
- **`selenium_methods.py`:** Script con las funciones y algoritmos generales para realizar web scraping mediante la libreria Selenium.
- **`selenium_conf.json`:** Archivo con los datos de logeo y direcciones Xpaths para la extracción de la información.
- **`BACKUP.csv`:** Archivo de respaldo donde se guardan los últimos datos recolectados por el bot en caso de un paro total.
- **`log.out`:** Archivo de registro del proceso de web scraping donde se muestra el registro de respaldos y de errores presentados.

---

### Librerias en uso:

- **Pandas**
- **Numpy (NO EN USO)**
- **Nameparser (NO EN USO)**
- **Selenium**
- **JSON**
- **TQDM**

---

## Proceso

Ahora el proceso parte de una lista de URLs de donde se desean obtener los datos bibliográficos para lo cual se introducen al bot de Selenium. Para tener una obtención de datos adecuadas se debe realizar un pre-registro de la base de datos (página web) de donde se desea obtener la info, en el momento solo se tiene registrada la base de SCOPUS.

El proceso para realizar el preregistro es el siguiente:

1. Crear un archivo `.json` usando como plantilla el existente para la base de datos SCOPUS
2. Introducir credenciales de logeo para la página web (en caso de que sea necesario) así como el link directo a la página de logeo.
3. Crear un diccionario de XPath's para cada dato que se desea encontrar, se organiza en formato de array ya que pueden haber múltiples XPath's para un solo dato, por lo que se organiza en el array de tal forma que el primer XPath sea el más común. Para encontrar un XPath realize el siguiente proceso:
   3.1 Dirigase a la página web de donde desea obtener el dato
   3.2 De click derecho al dato que desea extraer y seleccione `Inspeccionar`, se le abrirán las herramientas de desarrollador con el archivo `.html` de la web.
   3.3 Repita el proceso para asegurarse que esté en el lugar correcto del archivo `.html` donde se encuentra el dato.
   3.4 Navegue por el archivo `.html` cerca de la posición en la que se le abrió, verá que varias zonas de la página se le resaltarán al pasar el mouse por el archivo `.html`.
   3.5 Cuando tenga resaltada la zona correspondiente a su dato o encontró el dato específico en el código, seleccione con el mouse la zona del código o el dato en el código, en las opciones que le aparecieron ponga el mouse sobre la opción `Copiar`, en las nuevas opciones de click donde dice `Copiar XPath Completo` o `Copy Full XPath`.

En el archivo `.json` se puede observar un XPath auxiliar que se puede usar para realizar ubicaciones relativas de algunos datos en la página web, esto puede llegar a ser muy especializado para cada base de datos por lo que habría que acondicionar el proceso realizado por Selenium en comparación al que se realiza actualmente para SCOPUS.
