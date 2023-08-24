import configGptApi
import openai
from openai.error import ServiceUnavailableError
import time

api_key = configGptApi.api_key
openai.api_key = api_key

'''La siguiente funcion analiza si un texto tiene más de un maximo de frases proporcionada y, si es asi, elimina el
sobrante de frases. Las frases se consideran separaciones de un caracter también proporcionado'''
def simplify_text(texto, caracter, max_frases):
    texto_list = texto.split(caracter)
    n_frases = len(texto_list)
    if caracter != "¿" and caracter != "¡":
        caracter = caracter + " "
    if caracter == "¿" or caracter == "¡":
        n_frases -= 1
    if n_frases > max_frases:
        diff = n_frases - max_frases
        for i in range(0, diff):
            del texto_list[-1]
        texto = caracter.join(texto_list)
    return texto

def gpt_conversation(respuesta_usuario, messages):    #respuestas_usuarios será un texto con lo que el usuario va contestando

    messages.append({"role": "user","content": respuesta_usuario})    #Se integra la pregunta realizada (input) dentro del diccionario de content para poder seguir el hilo de la conversación en base a lo preguntado

    exito = False
    while exito == False:
        try:
            response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", temperature = 0.2,
                                     messages= messages)    #se conecta con Chat gpt y se hace una petición de respuesta
            exito = True
        except ServiceUnavailableError as e:
            print("Ocurrió un error: {}".format(e))
            time.sleep(5)

    response_content = response.choices[0].message.content  #se coge solo la parte de la respuesta que interesa (el texto)

    #Se limita a 2 frases como limite
    #Primero se separan las frases por puntos
    response_content = simplify_text(response_content, ".", 2)
    #Luego, por signos de interrogacion "¿"
    response_content = simplify_text(response_content, "¿", 1)

    messages.append({"role": "assistant", "content": response_content}) #Se integra la respuesta (output) dentro del
    # diccionario de content para poder seguir el hilo de la conversación

    return response_content, messages    #Se devuelve la respuesta para el usuario y messages
