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

        # Se combina para que cada intervención de usuario case con lo conversado en su linea
        conver = list(zip(chat_priv_nick_text, chat_priv_resp_text))
        return conver   #Se devuelve una lista de listas

primer_usuario = WebDriverWait(driver, 1000 ).until(
        EC.visibility_of_element_located((By.XPATH, '//div[@data-name="queries"]//div[@class="kiwi-statebrowser-channel-name"]')))

print(primer_usuario.text)
primer_usuario.click()

input("Presiona enter para comenzar la conversación...")

messages = []
continuar = True
while continuar == True:
        #Se define el prompt de asistente para chatgpt
        partes_prompt = ["INTRODUCCION:", "DESCRIPCION:", "OBJETIVO:", "METODO:", "TEXTO_NECESARIO_EVITAR_ERRORES"]
        dict_prompt_sistema = {partes_prompt[0]: "", partes_prompt[1]: "", partes_prompt[2]: "", partes_prompt[3]: ""}
        archivo_prompt_sistema = 'Prompts para chatgpt.txt'
        prompt_sistema_completo = ""

        i = 0
        with open(archivo_prompt_sistema) as archivo:
            for linea in archivo:
                print(linea)
                print(type(linea))
                if linea != "":
                        if partes_prompt[i+1] in linea:
                                i += 1
                        parte_prompt = partes_prompt[i]
                        dict_prompt_sistema[parte_prompt] += linea

        for i in range(0,4):
                print(f'Visualizando el diccionario para {partes_prompt[i]} \n{dict_prompt_sistema[partes_prompt[i]]}\n')
                messages.append({"role": "system",
                             "content": dict_prompt_sistema[partes_prompt[i]]})  # Con este rol, se van a dar unas instrucciones para orientar al
                # programa al objetivo deseado (se le da un contexto para condicionar la conversación

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
                tiempo_espera = random.choice(list(range(5, 10)))  # Se estima que se tarda en contestar entre 10 y 30 segundos
                time.sleep(tiempo_espera)
                if primer_mensaje:
                        conver = read_conver()
                        conver_bk = []
                else:
                        while conver == conver_bk:      #Estas dos variables se han igualado al final del for
                                print("ESPERANDO respuesta...")
                                time.sleep(10)
                                conver = read_conver()

                print("PROCESANDO respuesta...")

                #RECORDATORIOS A GPT

                #Se hace un recordatorio del prompt de sistema cada 10 itiraciones
                if i % 2 == 0:
                        for j in range(2,4):
                                dict_buscado = {"role": "system", "content": dict_prompt_sistema[partes_prompt[j]]}
                                if dict_buscado in messages:
                                        indice_dict_buscado = messages.index(dict_buscado)
                                        del messages[indice_dict_buscado]
                                else:
                                        messages.append({"role": "system", "content": dict_prompt_sistema[partes_prompt[j]]})
                        print("Se hace recordatorio del prompt de sistema de Objetivo y Metodo")

                if i % 5 == 0:
                        for j in range(0,2):
                                dict_buscado = {"role": "system", "content": dict_prompt_sistema[partes_prompt[j]]}
                                if dict_buscado in messages:
                                        indice_dict_buscado = messages.index(dict_buscado)
                                        del messages[indice_dict_buscado]
                                else:
                                        messages.append({"role": "system", "content": dict_prompt_sistema[partes_prompt[j]]})
                        print("Se hace recordatorio del prompt de sistema de Introducción y Descripción")

                #Se lee si yo he dicho (manualmente) la palabra clave de salida sin resumen
                #Además, se lee si el usuario se ha ido y, por lo tanto, se lee un error
                palabra_clave = "chao!!"
                palabra_error_nick = "No such nick"
                conver_limpia = []  # En esta lista se va a incluir lo único que no este repetido en la conversación
                for sublista in conver:
                        if palabra_clave in sublista or palabra_error_nick in sublista:
                                exit_bucle = True
                                break
                        else:
                                if sublista not in conver_bk:
                                        conver_limpia.append(sublista)
                                else:
                                        pass
                if exit_bucle:
                        break

                conver_bk = conver  # Se crea un back up de la conversación
                '''Como lo que se ha obtenido en la última variable es una lista de listas, se extrae lo último que ha respondido
                el usuario con el que se habla para transformarlo en una cadena de texto. Esto será el prompt. Ojo, si el 
                último en hablar he sido yo (que solo puede ser de forma manual) el programa sigue sin consultar a gpt.'''
                cadena_conver_resp = []
                for sublista in conver_limpia:
                        cadena_conver_resp.append(sublista[1])

                respuesta_usuario = ". ".join(cadena_conver_resp)

                print(f'Respuesta usuario para enviar a gpt: {respuesta_usuario}')

                #Se llama a la función en la que se obtendrá la respuesta por parte de gpt.
                respuesta_gpt, messages = gpt.gpt_conversation(respuesta_usuario, messages)
                # Se sustituyen los simbolos de interrogación y exclamación al comienzo de las preguntas y exclamaciones
                caracteres_buscados = ["¿", "¡", "'"]
                for caracter in caracteres_buscados:
                        respuesta_gpt = respuesta_gpt.replace(caracter, "")
                #Se transforma la frase a minúsculas
                respuesta_gpt = respuesta_gpt.lower()
                #Se imprime por pantalla la respuesta transformada, tal y como se vería en el chat
                print(f'Respuesta gpt: {respuesta_gpt}')
                #Ahora se envía la respuesta de gpt en el chat
                campo_mensaje = driver.find_element(by = By.XPATH, value = '//div[@placeholder="Enviar un mensaje..."]')
                # Se va a dividir la respuesta en varios "intros" por cada punto, para darle naturalidad
                respuesta_gpt_lista = respuesta_gpt.split(".")

                print('Simulando envío de respuesta por partes y con tiempo de escritura...')
                for frase in respuesta_gpt_lista:
                        try:
                                tiempo_escritura_por_palabra = 1  # segundos
                                num_palabras_respuesta_frase = len(re.findall(r"\w+", frase))
                                time.sleep(tiempo_escritura_por_palabra * num_palabras_respuesta_frase)
                                campo_mensaje.send_keys(frase)
                                campo_mensaje.send_keys(Keys.ENTER)
                        except WebDriverException as e:
                                if "ChromeDriver only supports characters in the BMP" in str(e):
                                        mensaje_orden = "En tu siguiente respuesta, quiero que digas lo mismo pero sin" \
                                                        "incluir emojis, es decir, en formato BMP"
                                        respuesta_gpt, messages = gpt.gpt_conversation(mensaje_orden, messages)
                                else:
                                        print("Error no contemplado")

                print("Envío completado")

                #Se da algo de tiempo para que se cargue la conversación en el scrip HTML del chat
                time.sleep(5)
                #Se vuelve a leer la conversacion y se crea un backup
                conver_intermedia = read_conver()
                conver_intermedia_solo_ususario = [sublista[1] for sublista in conver_intermedia if sublista[0] != nick]
                conver_solo_usuario = [sublista[1] for sublista in conver if sublista[0] != nick]

                # Se vuelve a leer la conversacion
                conver = conver_intermedia
                #Se compara exclusivamente lo que ha dicho el usuario antes de enviar las respuestas y después
                if conver_intermedia_solo_ususario == conver_solo_usuario:
                        conver_bk = conver
                else:
                        for sublista in conver_intermedia:
                                if sublista not in conver_bk and sublista[0]==nick:
                                        conver_bk.append(sublista)
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
        dict_buscado = {"role": "system", "content": dict_prompt_sistema[partes_prompt[2]]}
        indice_dict_buscado = messages.index(dict_buscado)
        print(f'Indice de dict buscado: {indice_dict_buscado}')
        contador = 0
        for message in messages:
                print(contador)
                print(message)
                contador += 1
        continuar_preg = input("¿Quieres continuar? S/N: ")
        if continuar_preg == "S":
                continuar = True
                messages = []
        else:
                continuar = False

driver.quit()