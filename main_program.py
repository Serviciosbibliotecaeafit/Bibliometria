import selenium_methods as sm
import norm_methods as norm
import pandas as pd
import sys
import os

def Search_Data(data_base, filename, credentials):
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

def Export(data, outputFolder):
    # Convertimos a DataFrame
    outputData = pd.DataFrame(data)

    # Exportamos a csv los datos normalizados
    csvPath = os.path.join(outputFolder, "Data.csv")
    outputData.to_csv(csvPath)
    
    # Exportamos a Excel
    excelPath = os.path.join(outputFolder, "Data.xlsx")
    outputData.to_excel(excelPath, sheet_name="Output Data")