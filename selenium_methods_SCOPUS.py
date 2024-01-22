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
    - v1.1.0: Enfocado unicamente en la base de datos SCOPUS pero facilmente replicable (no reutilizable) para otras.
"""

def open_nav():
    # Abre el navegador (usamos firefox por compatibilidad con pyInstaller)
    return webdriver.Firefox()


# TODOS LOS METODOS UTLIZADOS SOLO PARA SCOPUS

def log_in(driver, log_url, email, password):
    # Logea a la base de datos utilizando las credenciales del usuario
    driver.get(log_url)

    email_box_ID = "bdd-email" # UNICAMENTE SCOPUS
    email_box = driver.find_element(By.ID, email_box_ID)
    email_box.send_keys(email)

    continue_button_ID = "bdd-elsPrimaryBtn" # UNICAMENTE SCOPUS
    continue_button = driver.find_element(By.ID, continue_button_ID)

    # Espera 10 segundos en caso de que el boton no halla cargado correctamente
    WebDriverWait(driver, timeout=10).until(
        lambda d: button_available(d, continue_button_ID)
    )

    continue_button.click()

    password_box_ID = "bdd-password" # UNICAMENTE SCOPUS
    password_box = driver.find_element(By.ID, password_box_ID)
    password_box.send_keys(password)

    log_in_button_ID = "bdd-elsPrimaryBtn" # UNICAMENTE SCOPUS
    log_in_button = driver.find_element(By.ID, log_in_button_ID) # Puede que sea mejor esperar
    log_in_button.click()


def button_available(driver, button_ID):
    # Encuentra un boton, usado para las esperas
    return driver.find_element(By.ID, button_ID).is_enabled()        


def obtain_data_SCOPUS(urls, credentials):
    # Metodo principal para correr selenium

    # Credenciales de SCOPUS
    conf_file = open("selenium_conf_SCOPUS.json") # UNICAMENTE SCOPUS ya que por ahora ese .json solo tiene Xpaths de SCOPUS
    conf_data = json.load(conf_file)

    # URL de logeo
    log_url = conf_data["login_url"]

    # DATA REQUERIDA
    headers = [
        "Autores",
        "Titulo",
        "Nombre_Publicacion",
        "Tipo_Documento",
        "Idioma",
        "Resumen",
        "Filiacion_Autor",
        "Referencias_Citadas",
        "Total_Citas",
        "Pais_Filiacion_Autor",
        "Ano",
        "Volumen",
        "Numero",
        "DOI_Enlace_texto_completo",
    ]

    # Xpaths de cada header
    Xpaths = conf_data["XPATHS"]

    # Diccionario de salida
    output = {
        "Autores": [],
        "Titulo": [],
        "Nombre_Publicacion": [],
        "Tipo_Documento": [],
        "Idioma": [],
        "Resumen": [],
        "Filiacion_Autor": [],
        "Referencias_Citadas": [],
        "Total_Citas": [],
        "Pais_Filiacion_Autor": [],
        "Ano": [],
        "Volumen": [],
        "Numero": [],
        "DOI_Enlace_texto_completo": [],
    }

    # Abre el navegador
    driver = open_nav()

    # Logeo para SCOPUS
    log_in(driver, log_url, credentials["email"], credentials["password"])

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

        # Pestaña "ver más"
        view_more_button_ID = "show-additional-source-info" # UNICAMENTE SCOPUS
        view_more_button = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.ID, view_more_button_ID)
        )
        view_more_button.click()

        # Indices para busqueda de datos situacionalmente para cuando hay variacion de Xpath
        j = 0
        xpath_ind = 0

        while j < len(headers):
            head = headers[j]

            try:
                # en el caso del dato "Idioma" se hace un caso especial ya que puede variar un poco de posición
                if head == "Idioma":
                    title_view_more = WebDriverWait(driver, timeout=2).until(
                        lambda d: d.find_element(
                            By.XPATH, Xpaths["AUX_XPATH"][xpath_ind]
                        )
                    )
                    if title_view_more.text != "Original language":
                        raise TimeoutException

                # Obtencion general
                data_element = WebDriverWait(driver, timeout=2).until(
                    lambda d: d.find_element(By.XPATH, Xpaths[head][xpath_ind])
                )

                # Dato
                data = data_element.text

            except TimeoutException:
                # Excepción cuando no se encuentra el elemento en el tiempo esperado

                if head == "DOI_Enlace_texto_completo": # Si no hay DOI, usamos la url
                    data = url
                else:
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