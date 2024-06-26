from nltk.chat.util import Chat, reflections
from training import pares

# Crear el chatbot
chatbot = Chat(pares, reflections)

def chatbot_response(message):
    return chatbot.respond(message)
