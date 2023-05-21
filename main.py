import selenium_methods as sm
import pandas as pd

# Nombre del documento txt conteniendo los links donde obtener los datos
url_file_name = "test_urls"

# Extraemos las urls
urls_file = open(url_file_name + ".txt", "r")
urls = urls_file.read().split("\n")
urls_file.close()

# Extraemos los datos usando selenium_methods
urls_data = sm.obtain_data(urls)

# Exportamos a Excel
excelExport = pd.ExcelWriter("Data.xlsx")
pd.DataFrame(urls_data).to_excel(excelExport, sheet_name="Output Data")
