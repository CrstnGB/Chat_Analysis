import pandas as pd
import datetime
import openpyxl

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

    #Si ya existiese, se leen los datos del excel de output previo
    ruta_excel = r"C:\Users\Cristian\Documents\5- Educación\Python\0-Aprendizaje\5-Automatizaciones web con SELENIUM\1-Chat Nicks\Z-Outputs\Output.xlsx"
    #Se especifican la hoja y las columnas para que no haya discordancia entre lo leido y lo que se va a añadir
    nombre_hoja = "Registro"
    columnas = ['Nick', 'IP', 'Fecha', 'Hora']
    previo_df = pd.read_excel(ruta_excel, sheet_name=nombre_hoja, usecols = columnas)
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
    #Se preparan los datos para el dataframe
    datos = lista_usuarios
    #Se agrega la fecha y la hora a los datos
    for sublista in lista_usuarios:
        sublista.append(date_now)
        sublista.append(hour_now)

    #Se crea el dataframe
    nuevo_df = pd.DataFrame(datos, columns = columnas)
    #Se agrega el dataframe creado al previo
    final_df = pd.concat([previo_df, nuevo_df], ignore_index=True)
    #print(final_df)

    # Leer el archivo Excel existente y cargarlo en un diccionario de DataFrames
    with pd.ExcelFile(ruta_excel) as xlsx:
        hojas_dict = {sheet_name: xlsx.parse(sheet_name) for sheet_name in xlsx.sheet_names}

    hojas_dict[nombre_hoja] = final_df

    # Guardar el diccionario de DataFrames en el mismo archivo Excel
    with pd.ExcelWriter(ruta_excel, engine='openpyxl') as writer:
        for sheet_name, df in hojas_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print("Registro actualizado")

if __name__ == "__main__":
    lista_usuarios = [
        ['Juan', 'juan@iwehjakjdf.IP'],
        ['Carlos', 'carlos@ahifajkdf.IP']
    ]

    main(lista_usuarios)
