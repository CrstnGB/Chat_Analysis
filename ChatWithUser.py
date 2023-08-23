import gpt

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time
import random
import math
import initChannel
import re

driver, nick = initChannel.init()

def read_conver():
        ''' Primero se saca la lista de usuarios (será una lista donde se repetirán los usuarios continuamente,
                ya que solo hablan dos)'''
        chat_priv_nick = WebDriverWait(driver, 50).until(
                EC.visibility_of_all_elements_located(((By.XPATH, '//div[@class="kiwi-messagelist-item"]//a'))))
        # Esto será la lista de todas las respuestas. Más adelante se combinará con su usuario
        chat_priv_resp = WebDriverWait(driver, 50).until(
                EC.visibility_of_all_elements_located(
                        ((By.XPATH, '//div[@class="kiwi-messagelist-item"]//div[@class="kiwi-messagelist-body"]'))))

        # Se transforman las listas de objetos en texto
        chat_priv_nick_text = [elemento.text for elemento in chat_priv_nick]
        chat_priv_resp_text = [elemento.text for elemento in chat_priv_resp]

        # El nick del usuario contiene al final ":". Ej: "Jose:". Por lo tanto, se extrae tan solo el nick.
        i = 0
        for nick in chat_priv_nick_text:
                longitud = len(nick)
                chat_priv_nick_text[i] = nick[:longitud - 1]
                i += 1

        # Se ordena en orden inverso para obtener siempre lo último en la conversación
        chat_priv_nick_text_invertido = list(reversed(chat_priv_nick_text))
        chat_priv_resp_text_invertido = list(reversed(chat_priv_resp_text))

        # Se combina para que cada intervención de usuario case con lo conversado en su linea
        conver = list(zip(chat_priv_nick_text_invertido, chat_priv_resp_text_invertido))
        return conver

primer_usuario = WebDriverWait(driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, '//div[@data-name="queries"]//div[@class="kiwi-statebrowser-channel-name"]')))

print(primer_usuario.text)
primer_usuario.click()

input("Presiona enter para copiar la conversación...")

continuar = True
while continuar == True:
        #Se define el prompt de asistente para chatgpt
        archivo_prompt_asistente = 'Prompts para chatgpt.txt'
        prompt_asistente = ""
        with open(archivo_prompt_asistente) as archivo:
            for linea in archivo:
                prompt_asistente = prompt_asistente + "\n" + linea

        print(prompt_asistente)

        content_asistente = prompt_asistente

        messages = [{"role": "system",
                     "content": content_asistente}]  # Con este rol, se van a dar unas instrucciones para orientar al programa al objetivo deseado (se le da un contexto para condicionar la conversación

        #Comienza la conversación
        primer_mensaje = True
        exit_bucle = False
        i = 1
        for iterable in range(1, 41):
                print(f'Iteración {i}')
                '''Para cada iteración, se leerá la conversación completa y se creará una lista donde cada elemento es una
                interacción del usuario o de la máquina. Esta será una lista de listas, y cada sublista contendrá 
                el nick del usuario interviniente y lo chateado.'''

                '''Se necesita crear un backup de la conversación para poder comparar este estado con el anterior. Así se sabrá
                si ha variado algo la conversación con respecto la anterior itinerancia. En casi de que sí, el programa continua. 
                De lo contrario, se queda atrapado en el bucle. Ojo, si el usuario no contesta, escribir en la conversación la 
                palabra clave "chao"'''

                '''Debido a que es una conversación natural, es crucial que exista un tiempo de espera antes de contestar, sino
                                daría la sensación de que se está conversando on una IA.'''
                tiempo_espera = random.choice(list(range(5, 20)))  # Se estima que se tarda en contestar entre 10 y 30 segundos
                time.sleep(tiempo_espera)
                if primer_mensaje:
                        conver = read_conver()
                else:
                        while conver == conver_bk:
                                time.sleep(10)
                                conver = read_conver()
                conver_bk = conver

                #Se lee si yo he dicho (manualmente) la palabra clave de salida sin resumen
                #Además, se lee si el usuario se ha ido y, por lo tanto, se lee un error
                palabra_clave = "chao!!"
                palabra_error_nick = "No such nick"
                for sublista in conver:
                        if palabra_clave in sublista or palabra_error_nick in sublista:
                                exit_bucle = True
                                break
                if exit_bucle:
                        break

                if conver[0][1] == palabra_error_nick:
                        break
                '''Como lo que se ha obtenido en la última variable es una lista de listas, se extrae lo último que ha respondido
                el usuario con el que se habla para transformarlo en una cadena de texto. Esto será el prompt. Ojo, si el 
                último en hablar he sido yo (que solo puede ser de forma manual) el programa sigue sin consultar a gpt.'''
                respuesta_usuario = ""
                for sublista in conver:
                        user_nick = sublista[0]
                        if user_nick == nick:
                                break
                        else:
                                if primer_mensaje:
                                        respuesta_usuario = sublista[1]
                                else:
                                        respuesta_usuario = respuesta_usuario + ". " + sublista[1]


                if respuesta_usuario != "":
                        #Se llama a la función en la que se obtendrá la respuesta por parte de gpt.
                        respuesta_gpt, messages = gpt.gpt_conversation(respuesta_usuario, messages)
                        tiempo_escritura_por_palabra = 1.5      #segundos
                        num_palabras_respuesta_gpt = len(re.findall(r"\w+", respuesta_gpt))
                        time.sleep(tiempo_escritura_por_palabra * num_palabras_respuesta_gpt)
                        #Ahora se envía la respuesta de gpt en el chat
                        campo_mensaje = driver.find_element(by = By.XPATH, value = '//div[@placeholder="Enviar un mensaje..."]')
                        try:
                                campo_mensaje.send_keys(respuesta_gpt)
                                campo_mensaje.send_keys(Keys.ENTER)
                        except WebDriverException as e:
                                if "ChromeDriver only supports characters in the BMP" in str(e):
                                        mensaje_orden = "En tu siguiente respuesta, quiero que digas lo mismo pero sin" \
                                                        "incluir emojis, es decir, en formato BMP"
                                        respuesta_gpt, messages = gpt.gpt_conversation(mensaje_orden, messages)
                                else:
                                        print("Error no contemplado")

                else:
                        pass
                #Se cambia el estado de primer mensaje para saber que ya hay más de un mensaje por parte del usuario
                primer_mensaje = False
                i += 1

        prompt_resumen = "Olvídate ya que estás en una conversación. Devuelveme un resumen muy formal y estructurado de cómo es " \
                         "el usuario con el que hablas (el que tiene 'role: user' en tu lista de diccionarios de conversacion) " \
                         " además de todos los datos obtenidos de este." \
                         "Comienza simplemente por la frase: 'Aquí tienes un resumen estructurado del usuario:'"
        respuesta_gpt, messages = gpt.gpt_conversation(prompt_resumen, messages)
        print(conver)
        print(respuesta_gpt)
        continuar_preg = input("¿Quieres continuar? S/N: ")
        if continuar_preg == "S":
                continuar = True
                messages = []
        else:
                continuar = False


