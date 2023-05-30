import pandas as pd
import numpy as np
import urllib.request
import requests
from nameparser import HumanName
from nameparser.config import CONSTANTS

# Estetica
from tqdm.notebook import tqdm, trange

# Local
import not_use.web_methods as wm
import time

# Funciones
# Renombrar las columnas de un DataFrame


def Rename_Columns(data, dictionary) -> pd.DataFrame:
    newColumns = {}
    for index in data.columns.values:
        try:
            newColumns[index] = dictionary[index]
        except KeyError:
            newColumns[index] = index

    return data.rename(columns=newColumns)


# Renombrar las columnas de un array de DataFrame's


def Rename_Columns_array(data, dictionaries):
    bar = tqdm(range(len(data)))
    for i in bar:
        data[i] = Rename_Columns(data[i], dictionaries[i])
        bar.set_description("Renombrando columnas ....")


# Plantilla del consolidado


def Plantilla() -> dict:
    plantilla = {}

    headers = [
        "Autores",
        "Titulo",
        "Nombre_Publicación",
        "Tipo_Documento",
        "Idioma",
        "Resumen",
        "Filiación_Autor",
        "Referencias_Citadas",
        "Total_Citas" "País_Filiación_Autor",
        "Año",
        "Volumen",
        "Número",
        "DOI_Enlace_texto_completo",
    ]

    for head in headers:
        plantilla[head] = []

    return plantilla, headers


# Unificación de DataFrames


def Unify(data) -> dict:
    unified_data, headers = Plantilla()
    bar = tqdm(range(len(data)))
    for dataBaseNum in bar:
        dataBase = data[dataBaseNum]
        headers_data = dataBase.columns.values

        for index in dataBase.index.values:
            for head in headers:
                if head == "DOI_Enlace_texto_completo":
                    try:
                        unified_data[head].append(
                            dataBase.iloc[[index]]["DOI"].values[0]
                        )
                    except KeyError:
                        unified_data[head].append(
                            dataBase.iloc[[index]]["Enlace"].values[0]
                        )
                else:
                    try:
                        unified_data[head].append(
                            dataBase.iloc[[index]][head].values[0]
                        )
                    except KeyError:
                        unified_data[head].append(np.NaN)
        bar.set_description("Unificando ...")
    return unified_data


# Normalización de Autores usando nameparser


def Normalize_Authors(data, dataBases):
    """
    Lens:   Nombre Apellido ; -> Apellido, Nombre ;
    Scielo: Nombre Apellido , -> Apellido, Nombre ;
    Scopus: Apellido Nombre , -> Apellido, Nombre ;
    Wos:    Apellido, Nombre ; -> Apellido, Nombre ;
    """
    switch = {
        "LENS": Normalize_Authors_Lens,
        "SCIELO": Normalize_Authors_Scielo,
        "SCOPUS": Normalize_Authors_Scopus,
        "WOS": Normalize_Authors_Wos,
    }
    bar = tqdm(range(len(data)))
    for dataBaseNum in bar:
        normalization_case = switch.get(dataBases[dataBaseNum], Base_Not_Found)
        normalization_case(data[dataBaseNum])
        bar.set_description("Normalizando Autores ...")


# Procesos de normalización por base de datos


def Normalize_Authors_Lens(dataBase):
    CONSTANTS.string_format = "{first} {middle} {last}"
    for index in dataBase.index.values:
        author_list = dataBase.Autores.values[index].split(";")
        normalized_authors = []
        for author in author_list:
            name = HumanName(author.strip())
            last_name = name.last
            first_name = name.first

            if name.middle:
                first_name += " " + name.middle

            normalized_authors.append(f"{last_name}, {first_name}")

        dataBase.Autores.values[index] = "; ".join(normalized_authors)


def Normalize_Authors_Scielo(dataBase):
    CONSTANTS.string_format = "{last}, {first} {middle}"
    for index in dataBase.index.values:
        lst = dataBase.Autores.values[index].split(",")
        author_list = [", ".join(lst[i : i + 2]) for i in range(0, len(lst), 2)]
        normalized_authors = []
        for author in author_list:
            name = HumanName(author.strip())
            last_name = name.last
            first_name = name.first

            if name.middle:
                first_name += " " + name.middle

            normalized_authors.append(f"{last_name}, {first_name}")

        dataBase.Autores.values[index] = "; ".join(normalized_authors)


def Normalize_Authors_Scopus(dataBase):
    CONSTANTS.string_format = "{last} {first}.{middle}."
    for index in dataBase.index.values:
        author_list = dataBase.Autores.values[index].split(",")
        normalized_authors = []
        for author in author_list:
            name = HumanName(author.strip())
            last_name = name.last
            first_name = name.first

            if name.middle:
                first_name += " " + name.middle

            normalized_authors.append(f"{last_name}, {first_name}")

        dataBase.Autores.values[index] = "; ".join(normalized_authors)


def Normalize_Authors_Wos(dataBase):
    pass


def Base_Not_Found(dataBase):
    raise IndexError("Base de datos no encontrada.")


# Normalización de Tipo_Documento


def Normalize_Tipo_Documento(dataBase):
    """
    Opciones:
        - Article
        - Book Chapter
        - Proceedings Paper
        - Review
    Si está vacío se clasifica como Article
    """
    Tipos_Documentos = [
        "Article",
        "Book Chapter",
        "Proceedings Paper",
        "Review",
    ]
    for index in dataBase.index.values:
        try:
            Tipo_Documento = dataBase.Tipo_Documento.values[index]
            # print(Tipo_Documento)
            for clase in Tipos_Documentos:
                if clase.upper() in Tipo_Documento.upper():
                    dataBase.Tipo_Documento.values[index] = clase
                    break
        except:
            dataBase.Tipo_Documento.values[index] = Tipos_Documentos[0]


# Proceso completo de normalización y unificación


def full_Process(data, dataBases, dictionaries, do_web_search=True) -> pd.DataFrame:
    Rename_Columns_array(data, dictionaries)
    Normalize_Authors(data, dataBases)
    unified = pd.DataFrame(Unify(data))
    print("Tamaño: " + str(len(unified.index.values)))
    if do_web_search:
        wm.Full_with_doi(unified)
    Normalize_Tipo_Documento(unified)
    return unified


# Diccionarios con traducciones de las columnas de los dataFrame's
def Lens_Dictionary(lang="en") -> dict:
    lens_dict_en = {
        # 'Lens ID'
        "Title": "Titulo",
        # 'Date Published'
        "Publication Year": "Año",
        "Publication Type": "Tipo_Documento",
        "Source Title": "Nombre_Publicación",
        # 'ISSNs'
        # 'Publisher':   'Nombre_Publicación',  # No estoy seguro
        "Source Country": "País_Filiación_Autor",
        "Author/s": "Autores",
        "Abstract": "Resumen",
        "Volume": "Volumen",
        "Issue Number": "Número",
        # 'Start Page'
        # 'End Page'
        # 'Fields of Study'
        # 'Keywords'
        # 'MeSH Terms'
        # 'Chemicals'
        # 'Funding'
        "Source URLs": "Enlace Origen",
        "External URL": "Enlace Externo",
        # 'PMID'
        "DOI": "DOI",
        # 'Microsoft Academic ID'
        # 'PMCID'
        # 'Citing Patents Count'                    :   'Citing Patents Count', # No estoy seguro de incluirlo
        "References": "Referencias_Citadas",
        "Citing Works Count": "Total_Citas",
        # 'Is Open Access'
        # 'Open Access License'
        # 'Open Access Colour'
        # ''                                       :   'Idioma',
        # ''                                       :   'Filiación_Autor'
    }
    lens_dict_es = {
        # 'ID de The Lens'       :
        "Título": "Titulo",
        # 'Fecha de publicación' :
        "Año de publicación": "Año",
        "Tipo de publicación": "Tipo_Documento",
        # 'Título de la fuente'  :
        # 'ISSN'
        "Editor": "Nombre_Publicación",  # No estoy seguro
        "País de origen": "País_Filiación_Autor",
        "Autor/es": "Autores",
        "Resumen": "Resumen",
        "Volumen": "Volumen",
        "Número de problema": "Número",
        # 'Página de inicio'
        # 'Página final'
        # 'Campos de estudio'
        # 'Palabras clave'
        # 'Términos MeSH'
        # 'Químicos'
        # 'Financiación'
        "URL de origen": "Enlace Origen",
        "URL externa": "Enlace Externo",
        # 'PMID'
        "DOI": "DOI",
        # 'Identificación académica de Microsoft'
        # 'PMCID'
        # 'Recuento de citas de patentes'             :   'Citing Patents Count', # No estoy seguro de incluirlo
        "Referencias": "Referencias_Citadas",
        "Número de trabajos citados": "Total_Citas",
        # 'Es acceso abierto'
        # 'Licencia de acceso abierto'
        # 'Color de acceso abierto'
        # ''                                       :   'Idioma',
        # ''                                       :   'Filiación_Autor'
    }
    options = {"EN": lens_dict_en, "ES": lens_dict_es}
    return options[lang.upper()]


def Scielo_Dictionary() -> dict:
    scielo_dict = {
        "Title": "Titulo",
        "Author(s)": "Autores",
        "Journal": "Nombre_Publicación",
        "Publication year": "Año",
        "Fulltext URL ": "Enlace",
        # ''             :   'Tipo_Documento'
        "Language(s)": "Idioma",
        # ''             :   'Resumen',
        # ''             :   'Filiación_Autor',
        # ''             :   'Referencias Citadas',
        # ''             :   'Total_Citas',
        # ''             :   'País_Filiación_Autor',
        # ''             :   'Volumen',
        # ''             :   'Número',
    }
    return scielo_dict


def Scopus_Dictionary() -> dict:
    scopus_dict = {
        "Authors": "Autores",
        "Title": "Titulo",
        "Year": "Año",
        "Source title": "Nombre_Publicación",
        "Volume": "Volumen",
        "Issue": "Numero",
        "Cited by": "Total_Citas",
        "DOI": "DOI",
        "Link": "Enlace",
        "Affiliations": "Filiación_Autor",
        # 'Authors with affiliations' : '' # No estoy seguro
        "Abstract": "Resumen",
        "References": "Referencias_Citadas",
        # 'Publisher' :   'Nombre_Publicación',    # No estoy seguro
        "Language of Original Document": "Idioma",
        # ''         :   'Tipo_Documento',
        # ''         :   'País_Filiación_Autor',
    }
    return scopus_dict


def WoS_Dictionary() -> dict:
    wos_dict = {
        # 'PT':'Tipo_Documento',
        "AU": "Autores",
        # 'AF':'Author(s) Full Name',
        # 'BA':'Book Author(s)',
        # 'BF':'Book Author(s) Full Name',
        # 'CA':'Group Author(s)',
        # 'GP':'Book Group Author(s)',
        # 'BE':'Editor(s)',
        "TI": "Titulo",
        "SO": "Nombre_Publicación",
        # 'SE':'Book Series Title',
        # 'BS':'Book Series Subtitle',
        "LS": "Idioma",
        "DT": "Tipo_Documento",
        # 'CT':'Conference Title',
        # 'CY':'Conference Date',
        # 'CL':'Conference Location',
        # 'SP':'Conference Sponsors',
        # 'HO':'Conference Host',
        # 'DE':'Author Keywords',
        # 'ID':'Keywords Plus',
        "AB": "Resumen",
        "C1": "Filiación_Autor",  # No estoy seguro
        # 'RP':'Reprint Address',
        # 'EM':'E-mail Address',
        # 'RI':'ResearcherID Number',
        # 'OI':'ORCID',
        # 'FU':'Funding Agency',
        # 'FX':'Funding Text',
        "CR": "Referencias_Citadas",
        # 'NR':'Cited Reference Count',
        # 'TC':'WoS Core Collection Times Cited Count',
        "Z9": "Total_Citas",  # No estoy seguro
        # 'U1':'Usage Count (Last 180 Days)',
        # 'U2':'Usage Count (Since 2013)',
        # 'PU':'Publisher',
        # 'PI':'Publisher City',
        "PA": "País_Filiación_Autor",  # Lo incluye (No estoy seguro)
        # 'SN':'ISSN',
        # 'EI':'eISSN',
        # 'BN':'ISBN',
        # 'J9':'29-Character Source Abbreviation',
        # 'JI':'ISO Source Abbreviation',
        # 'PD':'Publication Date',
        "PY": "Año",
        "VL": "Volumen",
        "IS": "Número",
        # 'SI':'Special Issue',
        # 'PN':'Part Number',
        # 'SU':'Supplement',
        # 'MA':'Meeting Abstract',
        # 'BP':'Beginning Page',
        # 'EP':'Ending Page',
        # 'AR':'Article Number',
        "DI": "DOI",
        "D2": "Book DOI",
        # 'PG':'Page Count',
        # 'P2':'Chapter Count',
        # 'WC':'WoS Categories',
        # 'SC':'Research Areas',
        # 'GA':'Document Delivery Number',
        # 'UT':'Accession Number',
        # 'PM':'PubMed ID',
        # 'ER':'End of Record',
        # 'EF':'End of File'
    }
    return wos_dict
