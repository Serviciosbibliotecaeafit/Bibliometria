import selenium_methods as sm
import norm_methods as norm
import pandas as pd
import sys

# Nombre del documento txt conteniendo los links donde obtener los datos
url_file_name = sys.argv[1]

# Extraemos las urls
urls_file = open(url_file_name + ".txt", "r")
urls = urls_file.read().split("\n")
urls_file.close()

# Extraemos los datos usando selenium_methods
urls_data = sm.obtain_data(urls)

# Exportamos los datos crudos
pd.DataFrame(urls_data).to_csv("outputRAW.csv")

# Normalizamos los datos
outputData = norm.scopus(urls_data)

# Convertimos a DataFrame
outputData = pd.DataFrame(outputData)


# Exportamos a Excel
outputData.to_excel("Data.xlsx", sheet_name="Output Data")

# Exportamos a csv los datos normalizados
outputData.to_csv("output.csv")
