# Bibliometria

Unificación y normalización de bases bibliográficas.

***

## Descripciones

- **`{NOMBRE_BASE}/`:** Directorio con los datos sin unificar correspondientes a una base bibliográfica específica con nombre {NOMBRE_BASE}, e.g. LENS, SCIELO, WOS, etc.
- **`Unificar_Data_{NOMBRE_BASE}.ipynb`:** Notebook donde se realiza la unificación de los datos de una base espécifica con nombre {NOMBRE_BASE}.
- **`Unificar_Data.ipynb`:** Notebook donde se ejecutan las funciones y algoritmos que unifican globalmente y normalizan los datos de todas las bases bibliográficas.
- **`utilities.py`:** Script con las funciones y algoritmos necesarios para la unificación y normalización de los datos.

***

### Librerias en uso:

- **Pandas**
- **Numpy**
- **Nameparser**

***

## Proceso

**Objetivo:** Unificar y normalizar datos de distintas bases bibliográficas bajo identificadores como *AL_* o *BR_*. A continuación, se muestran algunos pasos que se realizan en el código:

1. **(Manual)** Almacenar datos en formato *.csv* en su respectiva carpeta de acuerdo a su base bibliográfica de origen, e.g. *`LENS/AL_1.csv`*, donde *AL_* indica el identificaron bajo el cual se ha de unificar local y globalmente.
2. **(Semi-Automático)** Unificar localmente los datos tanto por identificadores como por bases bibliográficas de origen y almacenar en la carpete *`output/`*, e.g. *`output/LENS_AL.csv`*, esto se realiza en notebooks individuales como *`Unificar_Data_Lens.ipynb`* para el caso expuesto. ***Nota:*** Hay que unir este proceso en un único notebook e idealmente bajo un único método.
3. **(Automático)** Unificación global y normalización de las bases unificadas localmente en *`output/`* usando los métodos programados en *`utilities.py`*. ***Nota:*** Para el proceso específico ver los comentarios en cada método *(en proceso)*.