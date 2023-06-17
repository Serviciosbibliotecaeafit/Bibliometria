import re # Libreria para usar expresiones regulares

"""
    Metodos de normalizacion separados por bases de datos y datos a normalizar

    Update Notes:
    - v0.1.0: Se tiene unicamente la normalizacion para SCOPUS.
"""

def scopus(data):
    """
        Normalizacion de datos provenientes de SCOPUS.

        En SCOPUS tenemos los siguientes campos normalizados por defecto:
            - Titulo
            - Nombre_Publicación
            - Idioma
            - Resumen
            - DOI_Enlace_text_completo
        Normalizaremos los demas campos en orden.
    """

    # data auxiliar
    aux_data = data

    # Normalización de Autores
    aux_data["Autores"] = Autores_scopus(data)

    # Normalización de Tipo_Documento
    aux_data["Tipo_Documento"] = Tipo_Doc_scopus(data)

    # Normalización de Filiación_Autor
    aux_data["Filiacion_Autor"] = Fili_Autor_scopus(data)

    # Normalización de Referencias_Citadas
    aux_data["Referencias_Citadas"] = Ref_Citadas_scopus(data)

    # Normalización de Total_Citas
    aux_data["Total_Citas"] = Total_Citas_scopus(data)

    # Normalización de Pais_Filiación_Autor
    aux_data["Pais_Filiacion_Autor"] = Pais_Fili_Autor_scopus(data)

    # Normalización de Año
    aux_data["Ano"] = Ano_scopus(data)

    # Normalización de Volumen
    aux_data["Volumen"] = Volumen_scopus(data)

    # Normalización de Número
    aux_data["Numero"] = Numero_scopus(data)

    return aux_data

def Autores_scopus(data):
    """
        Normalizacion de "Autores" para SCOPUS.

        Recibimos los datos de la forma
        'Autor1\n a\n Send mail to nombre1\n; Autor2\n ...'
    """
    old_values = data["Autores"]
    new_values = old_values

    pattern = r'^(?:[a-d],\s*)*[a-d]?$' # Expresion regular para capturar el patron

    for i in range(len(old_values)):
        if old_values[i] == "No Encontrado":
            continue

        values = old_values[i].split("\n") # Se separa por lineas
        valid_values = []

        for j in range(len(values)):
            # Tenemos en cuenta los elementos correspondientes unicamente a los autores
            if not re.match(pattern, values[j]) and values[j].find("Send mail") == -1 and values[j] != ";":
                valid_values.append(values[j])

        new_values[i] = "; ".join(valid_values) # Separamos con ;
    
    return new_values

def Tipo_Doc_scopus(data):
    """
        Normalizacion de "Tipo_Documento" para SCOPUS.

        Recibimos los datos de la forma
        'Tipo_Documento• Gold Open Access• ...'
    """
    old_values = data["Tipo_Documento"]
    new_values = old_values

    for i in range(len(old_values)):
        if old_values[i] == "No Encontrado":
            continue

        new_values[i] = old_values[i].split("•")[0]

    return new_values


def Fili_Autor_scopus(data):
    """
        Normalizacion de "Filiacion_Autor" para SCOPUS.

        Recibimos los datos de la forma
        'a Filiación_Autor, Ciudad(talvez), País_Filiación_Autor \nb ...'
    """
    old_values = data["Filiacion_Autor"]
    new_values = old_values

    for i in range(len(old_values)):
        if old_values[i] == "No Encontrado":
            continue

        values = [
            old_values[i].split("\n")[j][2:].split(",")[0] # patron
            for j in range(len(old_values[i].split("\n")))
        ]

        # Solo se incluye si todas las filiaciones son iguales
        comparative = values == [values[0] for j in range(len(values))] 
        if not comparative:
            new_values[i] = "Varias Filiaciones"
            continue

        new_values[i] = values[0]

    return new_values


def Ref_Citadas_scopus(data):
    """
        Normalizacion de "Referencias_Citadas" para SCOPUS.
    
        Recibimos los datos de la forma
        '1/nAutorCita1/,TituloCita1/n/n(AñoCita1) Nombre_PublicaciónCita1...'

        Esta sigue un patron demasiado variable, por lo que hay que buscar una mejor solucion de acuerdo a los requerimientos de bibliometria.
    """
    old_values = data["Referencias_Citadas"]
    new_values = old_values

    for i in range(len(old_values)):
        if old_values[i] == "No Encontrado":
            continue

        values = []
        value = old_values[i].split("\n")

        j = 0
        while j < len(value):
            if value[j].strip().isnumeric():
                values.append(",".join(value[j + 1 : j + 4])) # Se cumple aproximadamente, requiere mas revision
                j += 4
                continue
            j += 1

        # El siguiente patron se planteo pero no se sigue adecuadamente
        """ 
        j = 0
        while j < len(value):
            if value[j].strip().isnumeric():
                autorCita = value[j + 1]
                tituloCita = value[j + 2]
                try:
                    anoCita = value[j + 3][1:5]
                except IndexError:
                    print(value)
                if value[j + 3] == "":
                    anoCita = value[j + 4][1:5]
                values.append(", ".join([autorCita, anoCita, tituloCita]))
                j += 5
                continue
            j += 1"""

        new_values[i] = "; ".join(values)

    return new_values


def Total_Citas_scopus(data):
    """
        Normalizacion de "Total_Citas" para SCOPUS.

        Recibimos los datos de la forma
        'References (Total_Citas)'
    """
    old_values = data["Total_Citas"]
    new_values = old_values

    for i in range(len(old_values)):
        if old_values[i] == "No Encontrado":
            continue

        new_values[i] = old_values[i][-3:-1]

    return new_values


def Pais_Fili_Autor_scopus(data):
    """
        Normalizacion de "Pais_Filiacion_Autor" para SCOPUS.

        Recibimos los datos de la forma
        'a Filiación_Autor, Ciudad(talvez), País_Filiación_Autor \nb ...'
    """
    old_values = data["Pais_Filiacion_Autor"]
    new_values = old_values

    for i in range(len(old_values)):
        if old_values[i] == "No Encontrado":
            continue

        values = [
            old_values[i].split("\n")[j][2:].split(",")[-1][1:] # patron
            for j in range(len(old_values[i].split("\n")))
        ]

        # Solo se incluye si el pais de filiacion es unico
        comparative = values == [values[0] for j in range(len(values))]
        if not comparative:
            new_values[i] = "Varios Paises"
            continue

        new_values[i] = values[0]

    return new_values


def Ano_scopus(data):
    """
        Normalizacion de "Año" para SCOPUS.

        Recibimos los datos de la forma:
        "...OpenAccessVolume Volumen, Issue NumeroAno"
        Algunos de los datos pueden no estas (revisar outputRAW.csv para observar los patrones)
    """
    old_values = data["Ano"]
    new_values = old_values

    for i in range(len(old_values)):
        if old_values[i] == "No Encontrado":
            continue

        articleNumberIdx = old_values[i].find("Article number") # puede estar

        if articleNumberIdx == -1:
            new_values[i] = old_values[i][-4:] if old_values[i][-4:].strip().isnumeric() else "No Encontrado"
            continue

        new_values[i] = old_values[i][articleNumberIdx - 5 : articleNumberIdx - 1]

    return new_values


def Volumen_scopus(data):
    """
        Normalizacion de "Volume" para SCOPUS.

        Recibimos los datos de la forma:
        "...OpenAccessVolume Volumen, Issue NumeroAno"
        Algunos de los datos pueden no estas (revisar outputRAW.csv para observar los patrones)
    """
    old_values = data["Volumen"]
    new_values = old_values

    for i in range(len(old_values)):
        if old_values[i] == "No Encontrado":
            continue

        volumeIdx = old_values[i].find("Volume")
        endVolumeIdx = old_values[i].find(",", volumeIdx)

        if volumeIdx == -1:
            new_values[i] = "No Encontrado"
            continue

        new_values[i] = old_values[i][volumeIdx + 7 : endVolumeIdx]

    return new_values


def Numero_scopus(data):
    """
        Normalizacion de "Numero" para SCOPUS.

        Recibimos los datos de la forma:
        "...OpenAccessVolume Volumen, Issue NumeroAno"
        Algunos de los datos pueden no estas (revisar outputRAW.csv para observar los patrones)
    """
    old_values = data["Numero"]
    new_values = old_values

    for i in range(len(old_values)):
        if old_values[i] == "No Encontrado":
            continue
        
        numeroIdx = old_values[i].find("Issue")
        if numeroIdx == -1:
            new_values[i] = "No Encontrado"
            continue

        for j in range(len(old_values[i][numeroIdx + 7 :])):
            if not old_values[i][numeroIdx + 7 + j].isnumeric():
                new_values[i] = old_values[i][numeroIdx + 6 : numeroIdx + 7 + j]
                break

    return new_values
