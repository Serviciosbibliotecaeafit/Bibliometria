from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import json
import pandas as pd

from tqdm.notebook import tqdm


def open_nav():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def log_in(driver, log_url, email, password):
    print("Logging...")
    driver.get(log_url)
    email_box = driver.find_element(By.ID, "bdd-email")
    email_box.send_keys(email)
    continue_button = driver.find_element(By.ID, "bdd-els-searchBtn")
    WebDriverWait(driver, timeout=10).until(button_available)
    continue_button.click()
    password_box = driver.find_element(By.ID, "bdd-password")
    password_box.send_keys(password)
    log_in_button = driver.find_element(By.ID, "bdd-elsPrimaryBtn")
    log_in_button.click()


def button_available(driver):
    return driver.find_element(By.ID, "bdd-els-searchBtn").is_enabled()


def obtain_data(urls):
    # Credenciales de SCOPUS
    conf_file = open("selenium_conf.json")
    conf_data = json.load(conf_file)
    credentials = conf_data["credentials"]

    # URL para logear
    log_url = conf_data["login_url"]

    # Datos a buscar
    headers = [
        "Autores",
        "Titulo",
        "Nombre_Publicación",
        "Tipo_Documento",
        "Idioma",
        "Resumen",
        "Filiación_Autor",
        "Referencias_Citadas",
        "Total_Citas",
        "País_Filiación_Autor",
        "Año",
        "Volumen",
        "Número",
        "DOI_Enlace_texto_completo",
    ]

    # Direcciones de los datos
    Xpaths = conf_data["XPATHS"]

    # Salida
    output = {
        "Autores": [],
        "Titulo": [],
        "Nombre_Publicación": [],
        "Tipo_Documento": [],
        "Idioma": [],
        "Resumen": [],
        "Filiación_Autor": [],
        "Referencias_Citadas": [],
        "Total_Citas": [],
        "País_Filiación_Autor": [],
        "Año": [],
        "Volumen": [],
        "Número": [],
        "DOI_Enlace_texto_completo": [],
    }

    # Abrimos el navegador
    driver = open_nav()

    # Logeamos en SCOPUS
    log_in(driver, log_url, credentials["email"], credentials["password"])

    # Crear log
    register_log(
        "----------------------------------------------------------------\n\tINICIO DE REGISTRO\n----------------------------------------------------------------\n\n",
        True,
    )

    bar = tqdm(range(len(urls)))
    # Obtenemos los datos
    for i in bar:
        url = urls[i]
        driver.get(url)

        view_more_button = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.ID, "show-additional-source-info")
        )
        view_more_button.click()

        j = 0

        xpath_ind = 0
        while j < len(headers):
            head = headers[j]

            try:
                if head == "Idioma":
                    title_view_more = WebDriverWait(driver, timeout=2).until(
                        lambda d: d.find_element(
                            By.XPATH, Xpaths["AUX_XPATH"][xpath_ind]
                        )
                    )
                    if title_view_more.text != "Original language":
                        raise TimeoutException

                data_element = WebDriverWait(driver, timeout=2).until(
                    lambda d: d.find_element(By.XPATH, Xpaths[head][xpath_ind])
                )
                data = data_element.text
            except TimeoutException:
                if head == "DOI_Enlace_texto_completo":
                    data = url
                else:
                    if xpath_ind < len(Xpaths[head]) - 1:
                        xpath_ind += 1
                        continue
                    print(head + " : " + url)
                    data = "Not Found"
                    register_log(
                        f"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\tDATO: <{head}> NO ENCONTRADO EN:\n\t {url}\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n"
                    )

            output[head].append(data)
            j += 1
            xpath_ind = 0
        if i % 10 == 0:
            pd.DataFrame(output).to_csv("selenium_outputs/BACKUP.csv")
            register_log(
                f"|||||||||||||||||||||||||||||||||||||||||\n\tBACKUP REALIZADO\n\tULTIMA URL:\n\t {url}\n|||||||||||||||||||||||||||||||||||||||||\n\n"
            )

    driver.close()
    return output


def register_log(text, first=False):
    mode = "a"
    if first:
        mode = "w"
    log_file = open("selenium_outputs/log.out", mode)
    log_file.write(text)
    log_file.close()
