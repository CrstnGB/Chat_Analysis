import configGptApi
import openai

api_key = configGptApi.api_key
openai.api_key = api_key


def gpt_conversation(respuesta_usuario, messages):    #respuestas_usuarios será un texto con lo que el usuario va contestando

    messages.append({"role": "user","content": respuesta_usuario})    #Se integra la pregunta realizada (input) dentro del diccionario de content para poder seguir el hilo de la conversación en base a lo preguntado

    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo",
                             messages= messages)    #se conecta con Chat gpt y se hace una petición de respuesta

    response_content = response.choices[0].message.content  #se coge solo la parte de la respuesta que interesa (el texto)

    messages.append({"role": "assistant", "content": response_content}) #Se integra la respuesta (output) dentro del diccionario de content para poder seguir el hilo de la conversación

    return response_content, messages    #Se devuelve la respuesta para el usuario y messages