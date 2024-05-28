import telebot
import re

# Reemplaza "BOT_TOKEN" con tu token de acceso
bot_token = ""
bot = telebot.TeleBot(bot_token)
chat_id = 

# Ruta del archivo donde se guardarán los mensajes
archivo_mensajes = "mensajes_telegram.txt"

# Función para guardar el mensaje en el archivo
def guardar_mensaje_en_archivo(mensaje):
    with open(archivo_mensajes, "a") as file:
        file.write(mensaje + "\n")

# Manejador para el comando /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "¡Hola! Soy un bot de Telegram diseñado para guardar tus puntos del libro de órdenes y monitorearlos.")

# Manejador para el comando /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, """ Te voy a dar un ejemplo de el formato que tienes que elegir para poder guardar tus puntos es el siguiente: 
/mis_puntos
GMTUSDT
Long: 0.2269, 0.2199, 0.2159
Short: 0.2410, 0.2461, 0.2568
                 
Como vez primero coloca el comando /mis_puntos , seguido de la moneda, luego long, y los tres puntos de long, luego short y los tres puntos de short.
                 ¡Yo me encargo de monitorearlos por ti!""")

# Manejador para todos los mensajes
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Verificar si el mensaje comienza con el comando /mis_puntos
    if message.text.startswith("/mis_puntos"):
        # Utilizar expresiones regulares para encontrar el formato adecuado
        regex_pattern = r"/mis_puntos\n([A-Z]+)\nLong: \d+\.\d+, \d+\.\d+, \d+\.\d+\nShort: \d+\.\d+, \d+\.\d+, \d+\.\d+"
        match = re.match(regex_pattern, message.text)
        if match:
            # Si coincide con el formato, guardar el mensaje
            nombre_remitente = message.from_user.first_name
            mensaje_sin_comando = message.text.split('\n', 1)[1]
            guardar_mensaje_en_archivo(f"{nombre_remitente}: {mensaje_sin_comando}")
            bot.reply_to(message, "Mensaje guardado correctamente.")
            print("Guardando")
        else:
            bot.reply_to(message, "El mensaje no sigue el formato requerido. Por favor, revisa y vuelve a intentarlo.")

# Inicia el bot
bot.polling()
