from binance.client import Client
import pandas as pd
import telebot
import time

bot_token = "7063485069:AAG9M4xLIuNdplXOUn6SGsxjMyzT66jAAeA"
bot = telebot.TeleBot(bot_token)
chat_id = -1002142100260

# Función para enviar mensajes a Telegram con manejo de excepciones
def enviar_mensaje_telegram(chat_id, mensaje):
    try:
        bot.send_message(chat_id, mensaje, parse_mode='HTML')
        print("Mensaje enviado a Telegram con éxito")
    except Exception as e:
        print(f"No se pudo enviar el mensaje a Telegram: {e}")

api_key = ''
api_secret = ''

client = Client(api_key=api_key, api_secret=api_secret)

pd.set_option("display.max_rows", None, "display.max_columns", None)

while True:
    monedas = []

    futures_exchange_info = client.futures_ticker()

    for element in futures_exchange_info:
        if 'USDT' in element['symbol'] and float(element['quoteVolume']) > 200000000.00 and float(element['lastPrice']) < 5:
            monedas.append(element)

    ticker_dataframe = pd.DataFrame(monedas)
    ticker_dataframe = ticker_dataframe[['symbol', 'quoteVolume']]
    ticker_dataframe = ticker_dataframe.sort_values(by='quoteVolume', ascending=True)
    ticker_dataframe = ticker_dataframe.reset_index(drop=True)

    titulo = "<b>MONEDAS CON LOS VOLUMENES MÁS ALTOS EN EL DÍA DE HOY EN BINANCE:</b>\n\n"
    mensaje = titulo + ticker_dataframe.to_string(index=True)
    
    enviar_mensaje_telegram(chat_id=chat_id, mensaje=mensaje)

    time.sleep(86400)  # Pausa la ejecución durante 24 horas (86400 segundos)
