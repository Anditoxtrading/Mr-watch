import re
import time
from pybit.unified_trading import HTTP
import telebot

# Reemplaza "BOT_TOKEN" con tu token de acceso
bot_token = "7063485069:AAG9M4xLIuNdplXOUn6SGsxjMyzT66jAAeA"
bot = telebot.TeleBot(bot_token)
chat_id = -1002142100260
# Diccionario para mantener un registro de qué alertas se han enviado
alertas_enviadas = {}

# Función para obtener el precio actual de una moneda
def obtener_precio_actual(symbol):
    try:
        session = HTTP(testnet=False)
        tickers = session.get_tickers(category="linear", symbol=symbol)
        if tickers["retCode"] == 0:
            return float(tickers["result"]["list"][0]["lastPrice"])
        else:
            return None
    except Exception as e:
        print(f"Error al obtener el precio de {symbol}: {e}")
        return None

# Función para enviar mensaje a Telegram
def enviar_alerta_telegram(message):
    try:
        bot.send_message(chat_id, message)
    except Exception as e:
        print(f"Error al enviar alerta a Telegram: {e}")

# Función para monitorear el precio de una moneda
def monitorear_moneda(symbol, long_prices, short_prices, nombre_remitente=None):
    try:
        if symbol not in alertas_enviadas:
            monitorear_precio(symbol, long_prices[0], "Long", long_prices[1:], nombre_remitente)
            monitorear_precio(symbol, short_prices[0], "Short", short_prices[1:], nombre_remitente)
    except Exception as e:
        print(f"Error al monitorear {symbol}: {e}")

# Función para monitorear el precio
def monitorear_precio(symbol, precio_objetivo, tipo, precios_adicionales, nombre_remitente=None):
    global alertas_enviadas
    try:
        precio_actual = obtener_precio_actual(symbol)
        if precio_actual is not None:
            porcentaje_distancia = abs(precio_actual - precio_objetivo) / precio_objetivo * 100
            if porcentaje_distancia <= 0.2:
                if symbol not in alertas_enviadas:
                    if tipo == "Long":
                        mensaje = f"Puntos de {nombre_remitente}:📗 Long en {symbol}\nShock: {precio_objetivo}\nLg 2: {precios_adicionales[0]}\nLg 3: {precios_adicionales[1]}"
                    elif tipo == "Short":
                        mensaje = f"Puntos de {nombre_remitente}:📕Short en {symbol}\nShock: {precio_objetivo}\nSt 2: {precios_adicionales[0]}\nSt 3: {precios_adicionales[1]}"
                    enviar_alerta_telegram(mensaje)
                    alertas_enviadas[symbol] = True  # Marcamos la alerta como enviada

            if tipo == "Long":
                print(f"Long en: {symbol} target: {precio_objetivo}")
            elif tipo == "Short":
                print(f"Short en: {symbol} target: {precio_objetivo}")
            print(f"Porcentaje de distancia: {porcentaje_distancia:.2f}%")
    except Exception as e:
        print(f"Error al monitorear el precio de {symbol}: {e}")

def leer_archivo_y_monitorear(archivo):
    contenido_guardado = []
    try:
        with open(archivo, "r") as file:
            lines = file.readlines()
            # Comenzar a leer desde la segunda línea
            for i in range(0, len(lines), 3):  # Saltar de 3 en 3 líneas
                if i + 2 < len(lines):  # Verificar si hay suficientes líneas
                    symbol_line = lines[i].strip().split(":")[1].strip()  # Extraer la parte del símbolo
                    symbol = symbol_line.split()[0]  # Tomar solo el primer elemento (el símbolo)
                    nombre_remitente = lines[i].strip().split(":")[0]  # Extraer el nombre del remitente
                    long_prices = list(map(float, lines[i+1].split(":")[1].strip().split(",")))
                    short_prices = list(map(float, lines[i+2].split(":")[1].strip().split(",")))
                    contenido_guardado.append((symbol, long_prices, short_prices, nombre_remitente))
                else:
                    print("Conjunto de datos incompleto encontrado. Ignorando.")
    except Exception as e:
        print(f"Error al leer el archivo {archivo}: {e}")

    # Continuar monitoreando con los datos guardados
    for symbol, long_prices, short_prices, nombre_remitente in contenido_guardado:
        monitorear_moneda(symbol, long_prices, short_prices, nombre_remitente)

# Ejemplo de uso
archivo_mensajes = "mensajes_telegram.txt"

while True:
    leer_archivo_y_monitorear(archivo_mensajes)
    time.sleep(5)  # Esperar 5 segundos antes de volver a monitorear
