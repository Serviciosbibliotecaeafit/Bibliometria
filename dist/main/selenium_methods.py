from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

import json
import pandas as pd
import os
import sys

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")

def open_nav():
    # Abrimos el navegador
    return webdriver.Firefox('./driver/', options=options)


def log_in(driver, log_url, email, password):
    # Logeo a la base de datos usando las credenciales en selenium_conf.json
    #print("Logging...")
    driver.get(log_url)
    email_box = driver.find_element(By.ID, "bdd-email")
    email_box.send_keys(email)
    continue_button_ID = "bdd-elsPrimaryBtn"
    continue_button = driver.find_element(By.ID, continue_button_ID)
    WebDriverWait(driver, timeout=10).until(
        lambda d: button_available(d, continue_button_ID)
    )
    continue_button.click()
    password_box = driver.find_element(By.ID, "bdd-password")
    password_box.send_keys(password)
    log_in_button = driver.find_element(By.ID, "bdd-elsPrimaryBtn")
    log_in_button.click()


def button_available(driver, button_ID):
    # Comprobación si un botón está disponible
    return driver.find_element(By.ID, button_ID).is_enabled()


def obtain_data(urls, credentials):
    # Obtención de los datos mediante web-scraping

    # Credenciales de SCOPUS
    conf_file = open("selenium_conf.json")
    conf_data = json.load(conf_file)

    # URL para logear
    log_url = conf_data["login_url"]

    # Datos a buscar
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

    # Direcciones de los datos
    Xpaths = conf_data["XPATHS"]

    # Salida
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

    # Abrimos el navegador
    driver = open_nav()

    # Logeamos en SCOPUS
    log_in(driver, log_url, credentials["email"], credentials["password"])

    # Creamos registro
    register_log(
        "----------------------------------------------------------------\nINICIO DE REGISTRO\n----------------------------------------------------------------\n\n",
        True,
    )

    # Obtenemos los datos
    for i in range(len(urls)):
        register_progress(i+1, len(urls))
        url = urls[i]
        driver.get(url)

        # Abrimos la pestaña de 'ver más'
        view_more_button = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.ID, "show-additional-source-info")
        )
        view_more_button.click()

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

                # Buscamos el elemento conteniendo el dato
                data_element = WebDriverWait(driver, timeout=2).until(
                    lambda d: d.find_element(By.XPATH, Xpaths[head][xpath_ind])
                )

                # Tomamos el texto del elemento
                data = data_element.text
            except TimeoutException:
                # Excepción cuando no se encuentra el elemento en el tiempo esperado

                if head == "DOI_Enlace_texto_completo":
                    data = url
                else:
                    # Iteramos sobre las distintas ubicaciones que puede tener el elemento y que están registradas en el .json
                    if xpath_ind < len(Xpaths[head]) - 1:
                        xpath_ind += 1
                        continue
                    # No se encontró completamente el elemento
                    #print(f"\n\tNO ENCONTRADO\n{head}:\n{url}\n")
                    data = "No Encontrado"
                    # Registramos el fallo de busqueda
                    register_log(
                        f"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\nDATO: <{head}> NO ENCONTRADO EN:\n {url}\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n"
                    )
            # Agregamos el dato al output
            output[head].append(data)
            j += 1
            xpath_ind = 0
        if i % 10 == 0:
            # Registro de busqueda
            pd.DataFrame(output).to_csv("selenium_outputs/BACKUP.csv")
            register_log(
                f"||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n\tBACKUP REALIZADO\n\tULTIMA URL:\n\t {url}\n||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n\n"
            )

    driver.close()
    register_log(
        "----------------------------------------------------------------\n\tFIN DE REGISTRO\n----------------------------------------------------------------\n\n"
    )
    register_progress(len(urls)+1, len(urls))
    return output


def register_log(text, first=False):
    # Función para guardar el registro de funcionamiento del bot
    mode = "w" if first else "a"
    log_file = open("./selenium_outputs/log.out", mode)
    log_file.write(text)
    log_file.close()

def register_progress(progress, maximum):
    # Función para guardar el progreso de la busqueda
    progress_file = open("./selenium_outputs/progress.out", "w")
    progress_file.write(str(100*progress/maximum))
    progress_file.close()