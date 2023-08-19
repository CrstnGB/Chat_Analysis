from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import math
import initChannel

inicio = time.time()
driver, nick = initChannel.init()

def get_n_users():
    # Se obtiene el número total de usuarios
    n_usuarios_texto = driver.find_element(by=By.XPATH,
                                           value='/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[1]/span')
    index_caracter_clave = n_usuarios_texto.text.index(" ")
    n_usuarios = int(n_usuarios_texto.text[:index_caracter_clave])
    return n_usuarios

def get_user_windows():
    # Se encuentra la ventana donde se almacenan todos los usuarios
    ventana_usuarios_xpath = '/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[2]'
    ventana_usuarios = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, ventana_usuarios_xpath)))
    return ventana_usuarios

def button_show_users():
    boton_mostrar_usuarios = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, r'/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/a')))
    boton_mostrar_usuarios.click()

def get_user_element_list():
    clase_usuarios = 'kiwi-nicklist-user-nick'
    lista_elementos_usuarios = driver.find_elements(by=By.CLASS_NAME, value=clase_usuarios)
    return lista_elementos_usuarios

def get_steps_to_scroll(ventana, n_usuarios):
    # Obtener el tamaño total del contenido desplazable del elemento
    ventana = get_user_windows()
    total_scroll_height = driver.execute_script("return arguments[0].scrollHeight;", ventana)
    n_usuarios_limite_salto = 30
    paso = math.ceil(n_usuarios / n_usuarios_limite_salto)
    pixeles_a_desplazar = int(total_scroll_height / paso)
    return paso, pixeles_a_desplazar

def add_users(lista_elementos_usuarios, lista_usuarios, booleano_IP):
    for usuario in lista_elementos_usuarios:
        lista_temporal = []
        if booleano_IP == False:
            lista_temporal.append(usuario.text.lower())
        else:
            lista_temporal.append(usuario)
        if booleano_IP == False:
            if lista_temporal not in lista_usuarios:
                lista_usuarios.append(lista_temporal)
            else:
                pass
        else:
            lista_usuarios.append(lista_temporal)

    return lista_usuarios

def add_users_IP(lista_usuarios_parcialmente_completada, lista_usuarios_agregados, contador1, contador2, paso, pixeles_a_desplazar):
    index = 0
    for sublista_usuario in lista_usuarios_parcialmente_completada:
        usuario_buscado = lista_usuarios_parcialmente_completada[index][0]
        #print(f'usuario_buscado: {usuario_buscado}')
        #n_usuarios = get_n_users()
        # Se vuelve a la posición inicial
        ventana_usuarios = get_user_windows()
        driver.execute_script("arguments[0].scrollTo(0, 0);", ventana_usuarios)
        for i in range(1, paso + 1):
            if i > 1:
                ventana_usuarios = get_user_windows()
                driver.execute_script(f"arguments[0].scrollTop += {pixeles_a_desplazar};", ventana_usuarios)
            lista_elementos_usuarios = get_user_element_list()
            #print(f'Cantidad de usuarios elementos a comparar: {len(lista_elementos_usuarios)}')
            #print(f'Primer usuario de la lista de elementos: {lista_elementos_usuarios[0].text}')
            #lista_mostrar = [usuario.text for usuario in lista_elementos_usuarios]
            #print(lista_mostrar)
            #input("-")

            for usuario in lista_elementos_usuarios:
                usuario_agregado = False
                try:
                    if usuario.text.lower() == usuario_buscado and usuario.text.lower() not in lista_usuarios_agregados:
                        #for i in range(1, paso + 1):
                        usuario.click()
                        contador2 += 1
                        usuario_IP = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'kiwi-userbox-usermask')))
                        #Se agrega su IP a la lista de usuarios
                        lista_usuarios_parcialmente_completada[index].append(usuario_IP.text)
                        #Se agrega a la lista de usuarios agregados
                        lista_usuarios_agregados.append(usuario_buscado)
                        usuario_agregado == True
                        print(f'Usuario agregado: {usuario_buscado}')
                        button_show_users()
                    else:
                        pass
                except Exception as e:
                    contador1 += 1
                    break

                if usuario_agregado == True:
                    break
            if usuario_agregado == True:
                break
        index += 1

    print(f'Cantidad de excepciones: {contador1}')
    print(f'Cantidad de clicks en usuarios: {contador2}')
    return lista_usuarios_parcialmente_completada, lista_usuarios_agregados

def get_user_list(paso, pixeles_a_desplazar, ventana_usuarios, nick, lista_usuarios = [],
                  lista_usuarios_parcialmente_completada = [], lista_usuarios_agregados = [],
                  contador1 = 0, contador2 = 0, booleano_IP = False):
    for i in range(1, paso + 1):
        # Se genera la lista de los elementos web de usuarios
        lista_elementos_usuarios = get_user_element_list()
        if booleano_IP == False:
            lista_usuarios = add_users(lista_elementos_usuarios, lista_usuarios, booleano_IP)
        else:
            #Se genera otro tipo de lista de usuarios
            lista_usuarios_parcialmente_completada, \
            lista_usuarios_agregados = add_users_IP(lista_usuarios_parcialmente_completada,
                                                    lista_usuarios_agregados, contador1, contador2,
                                                    paso, pixeles_a_desplazar)
            lista_usuarios = lista_usuarios_parcialmente_completada
            ventana_usuarios = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[2]')))
            break

        driver.execute_script(f"arguments[0].scrollTop += {pixeles_a_desplazar};", ventana_usuarios)
        time.sleep(0.1)

    # Se vuelve a la posición inicial
    driver.execute_script("arguments[0].scrollTo(0, 0);", ventana_usuarios)

    if [""] in lista_usuarios:
        lista_usuarios.remove([""])

    if [nick] in lista_usuarios:
        lista_usuarios.remove([nick])

    if booleano_IP == False:
        lista_usuarios.sort()

    print(f'Lista de nicks: {lista_usuarios}')
    return lista_usuarios

def main():
    #Se obtiene el número total de usuarios según la página web
    n_usuarios = get_n_users()

    #Se obtiene el elemento de ventana de usuarios
    ventana_usuarios = get_user_windows()

    # Ahora, se genera la lista con los nombres de los usuarios. Se debe scrollear varias veces por que se generan
    # según se hace scroll down
    paso, pixeles_a_desplazar = get_steps_to_scroll(ventana_usuarios, n_usuarios)
    lista_usuarios = get_user_list(paso, pixeles_a_desplazar, ventana_usuarios, nick)

    # Se vuelve a hacer lo mismo pero, esta vez, para obtener la lista de sus IPs
    lista_usuarios = get_user_list(paso, pixeles_a_desplazar, ventana_usuarios, nick,
                                   lista_usuarios_parcialmente_completada = lista_usuarios, booleano_IP = True)
    # Cerrar el navegador
    driver.quit()

    fin = time.time()

    tiempo_ejecu_min = (fin - inicio)/60
    tiempo_ejecu_min_int = int(tiempo_ejecu_min)
    tiempo_ejecu_seg_resto = int((tiempo_ejecu_min - tiempo_ejecu_min_int) * 60)

    print(f'Paso utilizado: {paso}')
    print(f'Tiempo transcurrido: {tiempo_ejecu_min_int} minutos y {tiempo_ejecu_seg_resto} segundos')

    lista_usuarios_definitiva = []
    eliminados = 0
    for sublista_usuario in lista_usuarios:
        if len(sublista_usuario) == 2:
            lista_usuarios_definitiva.append(sublista_usuario)

    eliminados = len(lista_usuarios) - len(lista_usuarios_definitiva)

    print(f'Cantidad de usuarios que salieron de la sala durante el proceso: {eliminados}')
    print(f'Porcentaje de recopilación: {round((1 - (eliminados / len(lista_usuarios))) * 100, 2)} %')

    return lista_usuarios_definitiva

if __name__ == "__main__":
    lista_usuarios = main()
    print(f'Cantidad de usuarios: {len(lista_usuarios)}')
    for usuario in lista_usuarios:
        print(usuario)

    print(lista_usuarios)