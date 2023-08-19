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
        EC.visibility_of_element_located((By.XPATH, '//div[@class="kiwi-messagelist-body"]/span')))

print(primer_usuario.text)
primer_usuario.click()

#Comienza la conversación
#Cada linea de la conversación, en primera instancia, se introducirá en una lista (puede haber más de una línea)
chat_usu_list = WebDriverWait(driver, 50).until(
        EC.visibility_of_all_elements_located(((By.XPATH, '//div[@class="kiwi-messagelist-body"]/span')))

print(chat_usu_list[0].text)

#Conversación
#/html/body/div[1]/div[2]/div[2]/div[3]/div[1]/div/div/div/div[1]/div/div/div
#/html/body/div[1]/div[2]/div[2]/div[3]/div[1]/div/div/div/div[2]/div/div/div
#Nick del usuario (Usuario:)
#/html/body/div[1]/div[2]/div[2]/div[3]/div[1]/div/div/div/div[1]/div/div/span[2]/a

