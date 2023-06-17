import selenium_methods as sm
import norm_methods as norm
import pandas as pd
import sys
import os

"""
    Métodos de extracción y normalización diferenciados por base de datos.

    Update Notes:
    - v0.1.0: Registrada unicamente la base de datos "Scopus"
    para extracción y normalización.
"""

def Search_Data(data_base, filename, credentials):
    """
        Extrae datos bibliográficos de un conjunto de links/urls
        ingresados desde la interfaz grafica.

        Diferencia la base de datos de donde obtener los datos
        y se normaliza de acuerdo a esta.
    """
    # Extraemos las urls
    urls_file = open(filename, "r")
    urls = urls_file.read().split("\n")
    urls_file.close()

    match data_base:
            case "LENS":
                # Falta registrar la base de datos
                outputData = {}

            case "SCIELO":
                # Falta registrar la base de datos
                outputData = {}
            
            case "SCOPUS":
                # Extraemos los datos usando selenium_methods
                urls_data = sm.obtain_data(urls, credentials)

                # Exportamos los datos crudos
                pd.DataFrame(urls_data).to_csv("outputRAW.csv")

                # Normalizamos los datos
                outputData = norm.scopus(urls_data)

            case "WOS":
                # Falta registrar la base de datos
                outputData = {}
            
            case default:
                raise ValueError("Base de Datos No Registrada")
    

    return outputData

def Export_Backup(data_base, outputFolder):
    """
        Normaliza y exporta el backup en selenium_outputs/BACKUP.csv
        de acuerdo a la base de datos seleccionada en la UI.
    """
    backupData = pd.read_csv('selenium_outputs/BACKUP.csv', sep=',').to_dict()
    match data_base:
            case "LENS":
                # Falta registrar la base de datos
                outputData = {}

            case "SCIELO":
                # Falta registrar la base de datos
                outputData = {}
            
            case "SCOPUS":
                
                # Normalizamos los datos
                outputData = norm.scopus(backupData)

            case "WOS":
                # Falta registrar la base de datos
                outputData = {}
            
            case default:
                raise ValueError("Base de Datos No Registrada")
    
    Export(outputData, outputFolder)

def Export(data, outputFolder):
    """
        Exporta data en forma de diccionario a .csv y .xlsx
    """
    # Convertimos a DataFrame
    outputData = pd.DataFrame(data)

    # Exportamos a csv los datos normalizados
    csvPath = os.path.join(outputFolder, "Data.csv")
    outputData.to_csv(csvPath)
    
    # Exportamos a Excel
    excelPath = os.path.join(outputFolder, "Data.xlsx")
    outputData.to_excel(excelPath, sheet_name="Output Data")