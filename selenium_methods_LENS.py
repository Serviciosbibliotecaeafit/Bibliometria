from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from progress_register import register_log, register_progress

import json
import pandas as pd

"""
    Obtencion de datos usando Selenium y Xpaths, puede que este método de ubicación no sea el más eficiente pero sí el más efectivo, ya que los datos en su mayoria no poseen IDs por si solos.

    Update Notes:
    - v1.1.0: Enfocado unicamente en la base de datos LENS pero facilmente replicable (no reutilizable) para otras.
"""

def open_nav():
    # Abre el navegador (usamos firefox por compatibilidad con pyInstaller)
    return webdriver.Firefox()

# METODOS UTLIZADOS SOLO PARA LENS

def log_in(driver, log_url, email, password):

    # Logea a la base de datos utilizando las credenciales del usuario
    driver.get(log_url)

    email_box_ID = "username" # UNICAMENTE LENS
    email_box = driver.find_element(By.ID, email_box_ID)
    email_box.send_keys(email)

    password_box_ID = "password" # UNICAMENTE LENS
    password_box = driver.find_element(By.ID, password_box_ID)
    password_box.send_keys(password)

    password_box_ID = "/html/body/div/div/div[1]/div/label/input" # UNICAMENTE LENS
    password_box = driver.find_element(By.XPATH, password_box_ID)
    password_box.click()

    log_in_button_ID = "signin" # UNICAMENTE SCOPUS
    log_in_button = driver.find_element(By.ID, log_in_button_ID) # Puede que sea mejor esperar
    log_in_button.click()
    driver.implicitly_wait(5)


def get_references(driver):
    # UNICAMENTE LENS
    # Encuentra los elementos de las referencias citadas
    driver.implicitly_wait(8)
    return driver.find_elements(By.CSS_SELECTOR, "h3.listing-result-title")


def obtain_data_LENS(urls, credentials):

    # Credenciales de LENS
    conf_file = open("selenium_conf_LENS.json")
    conf_data = json.load(conf_file)

    # URL de logeo
    log_url = conf_data["login_url"]

    # DATA REQUERIDA
    headers = [
        "Autores",
        "Titulo",
        "Nombre_Publicacion",
        "Tipo_Documento",
        "Campo_De_Estudio",
        "Resumen",
        "Filiacion_Autor",
        "Total_Citas",
        "Ano",
        "Volumen",
        "Numero",
        "Enlace_texto_completo",
        "Referencias_Citadas"
    ]

    # Xpaths de cada header
    Xpaths = conf_data["XPATHS"]

    # Diccionario de salida
    output = {
        "Autores": [],
        "Titulo": [],
        "Nombre_Publicacion": [],
        "Tipo_Documento": [],
        "Campo_De_Estudio": [],
        "Resumen": [],
        "Filiacion_Autor": [],
        "Total_Citas": [],
        "Ano": [],
        "Volumen": [],
        "Numero": [],
        "Enlace_texto_completo": [],
        "Referencias_Citadas": []
    }

    # Abre el navegador
    driver = open_nav()

    # Logeo para LENS
    #log_in(driver, log_url, credentials["email"], credentials["password"])

    # Inicio de registro de actividad
    register_log(
        "----------------------------------------------------------------\nINICIO DE REGISTRO\n----------------------------------------------------------------\n\n",
        True,
    )    

    # Loop principal
    for i in range(len(urls)):
        register_progress(i+1, len(urls)) # Registro de progreso
        url = urls[i]
        driver.get(url)

        # Indices para busqueda de datos situacionalmente para cuando hay variacion de Xpath
        j = 0
        xpath_ind = 0

        while j < len(headers):
            head = headers[j]

            try:
                # en el caso del dato "Referencias citadas" se hace un caso especial ya que puede variar un poco de posición
                if head != "Referencias_Citadas":

                    # Obtencion general
                    data_element = WebDriverWait(driver, timeout=3).until(
                        lambda d: d.find_element(By.XPATH, Xpaths[head][xpath_ind])
                    )

                    # Dato
                    data = data_element.text
                    print("obtenido")

                if head == "Enlace_texto_completo":
                    data = url    

                elif head == "Referencias_Citadas":
                    total_citas = ''.join(filter(str.isdigit, output["Total_Citas"][i]))

                    if total_citas != "0":
                        references_url = url.replace("main", "citations/articles")
                        driver.get(references_url)
                        data_element = get_references(driver)

                        # Obtén el texto de cada elemento y une los elementos con "; "
                        data = " ".join(element.text + "; " for element in data_element)

                    else:

                        data = "No Encontrado" 

                        # Registro del fallo
                        register_log(
                            f"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\nDATO: <{head}> NO HAY EN:\n {url}\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n"
                        )
                    
                
            except TimeoutException:
                # Excepción cuando no se encuentra el elemento en el tiempo esperado

                if head != "Enlace_texto_completo":
                    # Iteramos sobre los distintos Xpath del elemento registrados en el .json
                    if xpath_ind < len(Xpaths[head]) - 1:
                        xpath_ind += 1
                        continue

                    # No se encontró completamente el elemento
                    data = "No Encontrado"

                    # Registro del fallo
                    register_log(
                        f"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\nDATO: <{head}> NO ENCONTRADO EN:\n {url}\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n"
                    )

            # Se agrega el dato
            output[head].append(data)
            j += 1
            xpath_ind = 0

        if i % 10 == 0: # Se puede variar la iteracion del backup pero hay que tener en cuenta el rendimiento
            # Backup
            pd.DataFrame(output).to_csv("selenium_outputs/BACKUP.csv")
            # Registro de actividad
            register_log(
                f"||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n\tBACKUP REALIZADO\n\tULTIMA URL:\n\t {url}\n||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n\n"
            )

    driver.close() # Se cierra selenium
    
    # Registro de actividad
    register_log(
        "----------------------------------------------------------------\n\tFIN DE REGISTRO\n----------------------------------------------------------------\n\n"
    )

    # Registro de progreso mayor que 100 para terminar el thread secundario
    register_progress(len(urls)+1, len(urls))

    return output