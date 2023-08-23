import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random

# Configurar el controlador del navegador (por ejemplo, chromedriver)
driver = webdriver.Chrome()

def button_channel(nombre_sala):
    botones_sala = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, r'kiwi-statebrowser-channel-name')))
    for boton in botones_sala:
        if boton.text == nombre_sala:
            boton_sala = boton
            break
    print(f'Este es el boton de la sala: {boton_sala.text}')
    time.sleep(0.5)
    boton_sala.click()

def get_channel_name(url_texto):
    #Se busca extraer el nombre de la sala a través de la url
    pos_final = url_texto.index(".php")
    print(type(pos_final))
    #pos_inicial:
    for i, valor in reversed(list(enumerate(url_texto))):
        if valor == '/':
            pos_inicial = i
            break
    nombre_sala = '#' + url_texto[pos_inicial + 1 : pos_final].lower()
    return nombre_sala

def init():
    # Navegar a la página
    url = ["https://www.chateagratis.net/chat/53/sala/Cadiz.php",
           "https://www.chateagratis.net/chat/36/sala/Madrid.php"]
    url_texto = url[0]
    driver.get(url_texto)

    # Esperar hasta que el botón aceptar de la ventana emergente de cookies sea visible (máximo 10 segundos de espera)
    try:
        boton_aceptar = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.XPATH, r'//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]')))
        # Si el botón es visible, hacemos clic en el botón de aceptar cookies
        boton_aceptar.click()
    except:
        pass

    campo_nick = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "nickInput")))

    # Se genera un nick distinto cada vez para evitar la creación descontrolada del mismo para luego borrarlo de la lista
    nicks_raices = ["Lauriita_", "chica_cai", "ruubita_"]
    nick_raiz = nicks_raices[random.choice(list(range(len(nicks_raices))))]
    lista_aleatoria = list(range(19, 35))
    numero_aleatorio = random.choice(lista_aleatoria)
    nick = nick_raiz + str(numero_aleatorio)

    campo_nick.send_keys(nick)
    campo_nick.send_keys(Keys.ENTER)

    print(f'Nick escogido: {nick}')

    # A partir de aquí, ya estamos en la página web abierta
    # Se entra en la sala
    nombre_sala = get_channel_name(url_texto)
    button_channel(nombre_sala)
    # Se espera a que carguen todos los usuarios
    time.sleep(5)

    return driver, nick