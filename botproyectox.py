from typing import Final

# pip install python-telegram-bot
from telegram import InputFile, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import matplotlib.pyplot as plt
import numpy as np
import re
from sympy.parsing.sympy_parser import parse_expr
import sympy as sp
from fractions import Fraction
import RRLNHCCC as RRL


print('Starting up bot...')

TOKEN: Final = '6283280014:AAH3pAxZoLQt6WX670iFC1SB_EzBLZl61VQ'
BOT_USERNAME: Final = '@finalproyectoxbot'


# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! I\'m a Project X bot. How are you doing?')


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
    The following commands are available:
    
    /start -> Welcome message
    /help -> This message
    /suma -> Add two numbers
    /stars -> Show the plot of the stars
    /rrccc -> Solve a recurrence relation with constant coefficients
    /TODAS -> Show all the constellations

    """)

async def suma_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Obtener los números ingresados por el usuario
    numeros = update.message.text.split()[1:]
    if len(numeros) != 2:
        await update.message.reply_text('Por favor ingresa dos números separados por un espacio después del comando /suma.')
        return

    # Sumar los números
    try:
        suma = int(numeros[0]) + int(numeros[1])
    except ValueError:
        await update.message.reply_text('Por favor ingresa dos números válidos.')
        return

    # Responder con la suma
    await update.message.reply_text(f'La suma de {numeros[0]} y {numeros[1]} es {suma}.')

# Lets us use the /custom command
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command, you can add whatever text you want here.')

async def stars_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stars = []
    with open('Bot-TelegramApi\Constellations\stars.txt') as file:
        for line in file:
            data = line.strip().split()
            x, y, _, id, mag, harvard, *name = data[:7]
            stars.append((float(x), float(y), id, float(mag), harvard, name if isinstance(name, list) else name.split(" ")))

    x_coords = [star[0] for star in stars]
    y_coords = [star[1] for star in stars]
    plt.scatter(x_coords, y_coords, s=5)
    plt.title("Todas las estrellas")
    plt.savefig('Bot-TelegramApi\Constellations\image\plot.png')
    await context.bot.send_photo(chat_id=update.message.chat_id, photo='Bot-TelegramApi\Constellations\image\plot.png')

async def TODAS_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open('Bot-TelegramApi\Constellations\stars.txt', 'r') as f:
        coordenadas_constelaciones = {}
        stars = []
        for line in f:
            nombre =""
            nombreLista=""
            columnas = line.split()
            data = line.strip().split()
            x, y, = data[:2]
            if (len(columnas) >= 7):
                for i in range(6, len(columnas)):
                    nombre = nombre + columnas[i]
                nombreLista=(tuple(nombre.strip().split(';')))
            stars.append((float(x), float(y),nombreLista))

    archivos = ["Bot-TelegramApi\Constellations\constellations\Boyero.txt", "Bot-TelegramApi\Constellations\constellations\Casiopea.txt", 
                "Bot-TelegramApi\Constellations\constellations\Cazo.txt", "Bot-TelegramApi\Constellations\constellations\Cygnet.txt","Bot-TelegramApi\Constellations\constellations\Geminis.txt",
                "Bot-TelegramApi\Constellations\constellations\Hydra.txt", "Bot-TelegramApi\Constellations\constellations\OsaMayor.txt", "Bot-TelegramApi\Constellations\constellations\OsaMenor.txt"]
    constelaciones = []
    for archivo in archivos:
        with open(archivo) as f:
            constelaciones_archivo = [tuple(line.strip().replace(" ", "").split(",")) for line in f]
        constelaciones.extend(constelaciones_archivo)

    fig, ax = plt.subplots()

    for estrella in stars:
        x, y = estrella[0], estrella[1]
        ax.scatter(x, y,s=5)

    for constelacion in constelaciones:
        estrella1, estrella2 = constelacion
        x1, y1 = next((x, y) for x, y, nombre in stars if estrella1 in nombre)
        x2, y2 = next((x, y) for x, y, nombre in stars if estrella2 in nombre)
        ax.plot([x1, x2], [y1, y2], '-', lw=1.5)

    plt.legend()
    plt.subplots_adjust(left=0.148,
                        bottom=0.062, 
                        right=0.86, 
                        top=1, 
                        wspace=0.2, 
                        hspace=0.2)
    plt.grid(lw=0.2)
    plt.savefig('Bot-TelegramApi\Constellations\image\TODAS.png')
    await context.bot.send_photo(chat_id=update.message.chat_id, photo='Bot-TelegramApi\Constellations\image\TODAS.png')


def handle_response(text: str) -> str:
    # Create your own response logic
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'

    if 'how are you' in processed:
        return 'I\'m good!'

    if 'i love python' in processed:
        return 'Remember to subscribe!'

    return 'I don\'t understand'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

async def rrccc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('suma', suma_command))
    app.add_handler(CommandHandler('stars', stars_command))
    app.add_handler(CommandHandler('rrccc', rrccc_command))
    app.add_handler(CommandHandler('TODAS', TODAS_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
