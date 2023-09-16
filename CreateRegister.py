import pandas as pd
import datetime
import openpyxl
import sqlite3

def main(lista_usuarios):
    print("Actualizando registro...")
    #Primero, se obtiene la fecha y hora actual
    now = datetime.datetime.now()
    #Se pasa al formato deseado en formato texto
    format_date = "%d/%m/%Y"
    format_hour = "%H:%M"
    date_now = datetime.datetime.date(now).strftime(format_date)
    hour_now = datetime.datetime.time(now).strftime(format_hour)
    print(date_now)
    print(hour_now)

    #Se arreglan los datos: el segundo valor de las listas de lista, incluye en parte al nick, y se debe separar, ya que
    #lo que es "invariable" es el IP
    index = 0
    for sublista in lista_usuarios:
        IP_compuesto_texto = sublista[1]
        pos_inicial = IP_compuesto_texto.index("@")
        #Posición final:
        for i, valor in reversed(list(enumerate(IP_compuesto_texto))):
            if valor == ".":
                pos_final = i
                break
        solo_IP_texto = IP_compuesto_texto[pos_inicial + 1:pos_final]
        sublista[1] = solo_IP_texto

    #Se agrega la fecha y la hora a los datos
    for sublista in lista_usuarios:
        sublista.append(date_now)
        sublista.append(hour_now)

    # Se accede / crea la base de datos (solo se crea si no existiese ya). La siguiente línea, tan solo almacena la ruta
    ruta_bdd = r"C:\Users\Cristian\Documents\5- Educación\Python\0-Aprendizaje\5-Automatizaciones web con SELENIUM\1-Chat Nicks\base_de_datos\usuarios_chat.db"

    # Se crea un query para crear la tabla registro solo en caso de que no exista
    with sqlite3.connect(ruta_bdd) as conn:
        cursor = conn.cursor()
        # Se especifican la hoja y las columnas para que no haya discordancia entre lo leido y lo que se va a añadir
        nombre_tabla_registro = "Registro"
        columnas_registro = ['Nick', 'IP', 'Fecha', 'Hora']
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "{nombre_tabla_registro}" (
        "id_registro" INTEGER,
        "{columnas_registro[0]}" TEXT,
        "{columnas_registro[1]}" TEXT,
        "{columnas_registro[2]}" TEXT,
        "{columnas_registro[3]}" TEXT,
        PRIMARY KEY("id_registro" AUTOINCREMENT)
        )
        ''')

        #Ahora se introducen los datos en la tabla
        for sublista in lista_usuarios:
            cursor.execute(f'''
                    INSERT INTO {nombre_tabla_registro}
                    ({columnas_registro[0]},{columnas_registro[1]},{columnas_registro[2]},{columnas_registro[3]})
                    VALUES ("{sublista[0]}", "{sublista[1]}", "{sublista[2]}", "{sublista[3]}")
                    ''')
        #Se envían y guardan los cambios
        conn.commit()

    print("Registro actualizado")

#Este código sirve para realizar pruebas ejecutando el código desde este archivo py
if __name__ == "__main__":
    lista_usuarios = [
        ['Juan', 'juan@iwehjakjdf.IP'],
        ['Carlos', 'carlos@ahifajkdf.IP']
    ]

    main(lista_usuarios)
