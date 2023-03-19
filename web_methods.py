import pandas as pd
import numpy as np
import math as m
import urllib.request
import requests
import multiprocessing as mp

# Estetica
from tqdm.notebook import tqdm, trange

manager = mp.Manager()
data_dicts = manager.list()

## Obtención de datos con doi
def Obtain_with_doi(doi):
    url = 'https://doi.org/' + urllib.request.quote(doi)
    header = {'Accept': 'application/x-bibtex'}
    response = requests.get(url, headers=header)
    return response.text

## Dato del doi
def Return_from_response(data, index):
    data_dict = {'index':index,}
    for text in data.split(',\n\t'):
        if text[0] == '@':
            try:
                data_dict['type'].append(text[1:text.find('{')])
            except KeyError:
                data_dict['type'] = [text[1:text.find('{')]]
            continue

        object = text[0:text.find(' = ')]
        input = object + ' = '
        start = text.find(input) + len(input)
        result = text[start:]

        replacements = {
            "{\\'{a}}" : "á",
            "{\\'{e}}" : "é",
            "{\\'{i}}" : "í",
            "{\\'{o}}" : "ó",
            "{\\'{u}}" : "ú",
            "\n"       : "",
            "\t"       : "",
        }
        
        for key, value in replacements.items():
            result = result.replace(key, value)

        try:
            if (result[0] == '{' and result[-1] == '}'):
                result = result[1:-1]
        except IndexError:
            #print(result)
            pass

        try:
            data_dict[object].append(result)
        except KeyError:
            data_dict[object] = [result]
        
    return data_dict

def Run_In_Parallel(indexes_array, dataBase):
    proc = []
    for indexes in indexes_array:
        p = mp.Process(target=Return_from_response_set, args=(dataBase, indexes,))
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

def Return_from_response_set(dataBase, indexes):
    #print(len(indexes))
    
    for index in indexes:
        doi = dataBase.DOI_Enlace_texto_completo.values[index]
        if not pd.isna(doi) and doi[0:2] == '10':
            web_data = Obtain_with_doi(doi)
            data_dicts.append(Return_from_response(web_data, index))
            

def Return_full_dict(dataBase):
    '''bar = tqdm(dataBase.index.values)
    for index in bar:
        doi = dataBase.DOI_Enlace_texto_completo.values[index]
        if not pd.isna(doi) and doi[0:2] == '10':
            web_data = Obtain_with_doi(doi)
            data_dicts.append(Return_from_response(web_data, index))
        bar.set_description('Recolectando data ...')
    return data_dicts'''

    # Usando multiproccesing o multithreading
    '''Se define el número de procesadores dependiendo
    del output del método mp.cpu_count(), el cual puede variar
    entre computadores'''
    pcs = mp.cpu_count()
    indexes_array = np.array_split(dataBase.index.values, pcs)
    
    Run_In_Parallel(indexes_array, dataBase)
    #print(data_dicts)

    
## Unir los datos del doi con el unificado
def Full_with_doi(dataBase):
    eng_template = {
        #'Autores',
        #'Titulo'    :   'title',
        'Nombre_Publicación'    :   'journal',
        'Tipo_Documento'    :   'type',
        'Idioma'    :   'language',
        'Resumen'   :   'abstract',
        #'Filiación_Autor',
        #'Referencias_Citadas',
        #'Total_Citas'
        #'País_Filiación_Autor',
        'Año'   :   'year',
        'Volumen'   :   'volume',
        'Número'    :   'number',
        #'DOI_Enlace_texto_completo'
    }

    print('Iniciando Multiprocesamiento')
    Return_full_dict(dataBase)
    print('Multiprocesamiento Finalizado')

    bar = tqdm(data_dicts)
    for obj in bar:
        index = obj['index']
        for key, value in eng_template.items():
            try:
                if type(obj[value]) == list:                    
                    dataBase[key].values[index] = obj[value][0].capitalize()
                    continue

                dataBase[key].values[index] = obj[value]
            except KeyError:
                pass
            
        bar.set_description('Juntando data ...')