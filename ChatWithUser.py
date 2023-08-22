from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import math
import initChannel

driver, nick = initChannel.init()

primer_usuario = WebDriverWait(driver, 50).until(
        EC.visibility_of_element_located((By.XPATH, '//div[@data-name="queries"]//div[@class="kiwi-statebrowser-channel-name"]')))

print(primer_usuario.text)
primer_usuario.click()

input("Presiona enter para copiar la conversación...")
#Comienza la conversación
#Cada linea de la conversación, en primera instancia, se introducirá en una lista (puede haber más de una línea)
#Primero se saca la lista de usuarios (será una lista donde se repetirán los usuarios continuamente, ya que solo hablan dos
chat_priv_nick = WebDriverWait(driver, 50).until(
        EC.visibility_of_all_elements_located(((By.XPATH, '//div[@class="kiwi-messagelist-item"]//a'))))
#Esto será la lista de todas las respuestas. Más adelante se combinará con su usuario
chat_priv_resp = WebDriverWait(driver, 50).until(
        EC.visibility_of_all_elements_located(((By.XPATH, '//div[@class="kiwi-messagelist-item"]//div[@class="kiwi-messagelist-body"]'))))

#Se transforman las listas de objetos en texto
chat_priv_nick_text = [elemento.text for elemento in chat_priv_nick]
chat_priv_resp_text = [elemento.text for elemento in chat_priv_resp]

#Como cada vez que un usuario hablar al final se añaden ":", se extrae sin estos
i = 0
for nick in chat_priv_nick_text:
        longitud = len(nick)
        chat_priv_nick_text[i]= nick[:longitud - 1]
        i += 1

#Se ordena en orden inverso para obtener siempre lo último en la conversación
chat_priv_nick_text_invertido = list(reversed(chat_priv_nick_text))
chat_priv_resp_text_invertido = list(reversed(chat_priv_resp_text))

conver = list(zip(chat_priv_nick_text_invertido, chat_priv_resp_text_invertido))

print(conver)


