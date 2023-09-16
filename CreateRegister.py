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
    '''for sublista in lista_usuarios:
        sublista.append(date_now)
        sublista.append(hour_now)'''

    # Se accede / crea la base de datos (solo se crea si no existiese ya). La siguiente línea, tan solo almacena la ruta
    ruta_bdd = r"C:\Users\Cristian\Documents\5- Educación\Python\0-Aprendizaje\5-Automatizaciones web con SELENIUM\1-Chat Nicks\base_de_datos\usuarios_chat.db"
    with sqlite3.connect(ruta_bdd) as conn:
        # --------------------------CREACION DE TABLAS------------------
        cursor = conn.cursor()
        # Tabla Registro
        columnas_registro = ['id_registro', 'Fecha', 'Hora']
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "Registro"(
        "{columnas_registro[0]}" INTEGER,
        "{columnas_registro[1]}" TEXT,
        "{columnas_registro[2]}" TEXT,
        PRIMARY KEY("{columnas_registro[0]}" AUTOINCREMENT)
        )
        ''')
        # Tabla Usuarios
        # Se especifican la hoja y las columnas para que no haya discordancia entre lo leido y lo que se va a añadir
        columnas_usuarios = ['Nick', 'IP', 'id_registro']
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "Usuarios" (
        "{columnas_usuarios[0]}" TEXT,
        "{columnas_usuarios[1]}" TEXT,
        "{columnas_usuarios[2]}" INTEGER,
        FOREIGN KEY("{columnas_registro[0]}") REFERENCES Registro("columnas_registro[0]")
        )
        ''')

        cursor.execute(f'''
        INSERT INTO Registro
        ({columnas_registro[1]},{columnas_registro[2]})
        VALUES ("{date_now}", "{hour_now}")
        ''')

        #Se guarda en una variable una subconsulta necesaria para obtener el máximo número de los id_registro
        cursor.execute(f'SELECT MAX({columnas_registro[0]}) FROM Registro')
        max_id_registro = cursor.fetchall()

        #Ahora se introducen los datos en la tabla
        for sublista in lista_usuarios:
            cursor.execute(f'''
                    INSERT INTO Usuarios
                    ({columnas_usuarios[0]},{columnas_usuarios[1]},{columnas_usuarios[2]})
                    VALUES ("{sublista[0]}", "{sublista[1]}", {max_id_registro[0][0]})
                    ''')

        #Se crea una vista con información general uniendo las dos tablas
        cursor.execute('''
        CREATE VIEW IF NOT EXISTS info_general AS
        SELECT Registro.id_registro, Nick, IP, Fecha, Hora FROM Registro
        JOIN Usuarios ON Registro.id_registro = Usuarios.id_registro
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
