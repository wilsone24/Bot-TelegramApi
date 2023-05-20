#LIBRERIAS NECESARIAS
from typing import Final
from telegram import InputFile, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import matplotlib.pyplot as plt
import numpy as np
import re
from sympy.parsing.sympy_parser import parse_expr
import sympy as sp
from fractions import Fraction
import RRLNHCCC as RRL
import matplotlib.cm as cm
import requests
from io import BytesIO


print('Iniciando el bot...')

#CONFIGURACIONES NECESARIAS
TOKEN: Final = '6283280014:AAH3pAxZoLQt6WX670iFC1SB_EzBLZl61VQ'
BOT_USERNAME: Final = '@finalproyectoxbot'



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funcion que define el comando /start, el cual envia un mensaje de bienvenida al usuario.

    Args:
        update (Update): 
        context (ContextTypes.DEFAULT_TYPE): 
    """
    mensaje = '¡Hola! Bienvenido, Soy un bot de Proyecto X. ¿Cómo estás?. \n' \
                  'Estoy aquí para mostarte cosas que nunca habias visto 💻⚛. \n' \
                  'y resolver TODAS esas inquietudes acerca de estructuras discretas.🧠🤖 \n\n' \
                  'para poder observar toda mi funcionalidad, Ejecuta el comando /help.'
    await update.message.reply_text(mensaje)



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funcion que define el comando /help, el cual envia un mensaje de ayuda al usuario.

    Args:
        update (Update): 
        context (ContextTypes.DEFAULT_TYPE): 
    """
    await update.message.reply_text("""🆘🆘🆘
    A continuación se muestra una lista de comandos disponibles:
    
    /start -> Mensaje de bienvenida
    /help -> Muestra los comandos disponibles
    /starscons -> Muestra los comandos Sobre las Estrellas y Constelaciones
    /rrlnhccc -> Resuelve una relación de recurrencia lineal no homogenea con coeficientes constantes

    """)


async def starscons_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funcion que define el comando /starscons, el cual Despliega un menu para elegir una opcion.

    Args:
        update (Update): 
        context (ContextTypes.DEFAULT_TYPE): 
    """
    await update.message.reply_text("""
        A continuación se muestra una lista de comandos disponibles:
        /stars -> Muestra todas las estrellas
        /todas -> Muestra todas las constelaciones
        /constelacion -> Muestra una sola constelacion constelación
        """)


async def constelacion_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funcion que define el comando /constelacion, el cual Despliega un menu para elegir una constelacion a mostrar.

    Args:
        update (Update): 
        context (ContextTypes.DEFAULT_TYPE): 
    """

    with open('Estrellas Bonitas\stars.txt', 'r') as f:
        coordenadas_constelaciones = {}
        stars = []
        for line in f:
            nombre =""
            nombreLista=""
            columnas = line.split()
            data = line.strip().split()
            x, y, _, id, mag,  = data[:5]
            if (len(columnas) >= 7):
                for i in range(6, len(columnas)):
                    nombre = nombre + columnas[i]
                nombreLista=(tuple(nombre.strip().split(';')))
            stars.append((float(x), float(y),id, float(mag), nombreLista))


    archivos = ["Estrellas Bonitas\constellations\Boyero.txt", "Estrellas Bonitas\constellations\Casiopea.txt", 
                "Estrellas Bonitas\constellations\Cazo.txt", "Estrellas Bonitas\constellations\Cygnet.txt","Estrellas Bonitas\constellations\Geminis.txt",
                "Estrellas Bonitas\constellations\Hydra.txt", "Estrellas Bonitas\constellations\OsaMayor.txt", "Estrellas Bonitas\constellations\OsaMenor.txt"]


    constelaciones = ['Boyero', 'Casiopea', 'Cazo', 'Cygnet', 'Geminis', 'Hydra', 'OsaMayor', 'OsaMenor']

    # Obtener el número ingresado por el usuario
    opcion = update.message.text.split()[1:]
    if len(opcion) != 1:
        await update.message.reply_text('Seleccione una constelación: \n 1. Boyero \n 2. Casiopea \n 3. Cazo \n 4. Cygnet \n 5. Geminis \n 6. Hydra \n 7. OsaMayor \n 8. OsaMenor')
        await update.message.reply_text('Por favor ingresa un número separado por un espacio después del comando /constelacion.')
        return
    opcion = int(opcion[0])
    with open(f'Estrellas Bonitas\constellations\{constelaciones[opcion-1]}.txt') as f:
        constelaciones_archivo = [tuple(line.strip().replace(" ", "").split(",")) for line in f]
    fig, ax = plt.subplots(figsize=(8, 8))
    x_coords = [star[0] for star in stars]
    y_coords = [star[1] for star in stars]
    mag = [star[3] for star in stars]
    cmap = cm.get_cmap('Greys_r', 10)
    sizes = [3/ (m + 2) for m in mag]
    sc = ax.scatter(x_coords, y_coords, s=sizes, c=mag, cmap=cmap)
    for constelacion in constelaciones_archivo:
        estrella1, estrella2 = constelacion
        x1, y1 = next((x, y) for x, y,id, mag, nombre in stars if estrella1 in nombre)
        x2, y2 = next((x, y) for x, y,id, mag, nombre in stars if estrella2 in nombre)
        ax.plot([x1, x2], [y1, y2], '-', lw=1)
    ax.set_facecolor('black')
    sc.set_clim(0, 10)
    plt.legend()
    plt.subplots_adjust(left=0.126,
                        bottom=0.045, 
                        right=0.902, 
                        top=0.917, 
                        wspace=0.2, 
                        hspace=0.2)

    plt.title(f"Constelación {constelaciones[opcion-1]}")
    plt.savefig(r'Estrellas Bonitas\images\una.png')
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=r'Estrellas Bonitas\images\una.png')


async def stars_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funcion que define el comando /stars, el cual muestra todas las estrellas.

    Args:
        update (Update): 
        context (ContextTypes.DEFAULT_TYPE): 
    """
    stars = []
    with open('Estrellas Bonitas\stars.txt') as file:
        for line in file:
            data = line.strip().split()
            x, y, _, id, mag= data[:5]
            stars.append((float(x), float(y), id, float(mag)))
    x_coords = [star[0] for star in stars]
    y_coords = [star[1] for star in stars]
    mag = [star[3] for star in stars]
    cmap = cm.get_cmap('Greys_r', 10)
    sizes = [3 / (m + 2) for m in mag]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor('black')
    sc = ax.scatter(x_coords, y_coords, s=sizes, c=mag, cmap=cmap)
    sc.set_clim(0, 10)
    plt.legend()
    plt.subplots_adjust(left=0.126,
                        bottom=0.045, 
                        right=0.902, 
                        top=0.917, 
                        wspace=0.2, 
                        hspace=0.2)
    plt.title("Todas las estrellas")
    plt.savefig('Estrellas Bonitas\images\stars.png')
    await context.bot.send_photo(chat_id=update.message.chat_id, photo='Estrellas Bonitas\images\stars.png')


async def TODAS_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funcion que define el comando /todas, el cual muestra todas las constelaciones.

    Args:
        update (Update): 
        context (ContextTypes.DEFAULT_TYPE): 
    """
    with open('Estrellas Bonitas\stars.txt', 'r') as f:
        coordenadas_constelaciones = {}
        stars = []
        for line in f:
            nombre =""
            nombreLista=""
            columnas = line.split()
            data = line.strip().split()
            x, y, _, id, mag,  = data[:5]
            if (len(columnas) >= 7):
                for i in range(6, len(columnas)):
                    nombre = nombre + columnas[i]
                nombreLista=(tuple(nombre.strip().split(';')))
            stars.append((float(x), float(y),id, float(mag), nombreLista))

    archivos = ["Estrellas Bonitas\constellations\Boyero.txt", "Estrellas Bonitas\constellations\Casiopea.txt", 
                "Estrellas Bonitas\constellations\Cazo.txt", "Estrellas Bonitas\constellations\Cygnet.txt","Estrellas Bonitas\constellations\Geminis.txt",
                "Estrellas Bonitas\constellations\Hydra.txt", "Estrellas Bonitas\constellations\OsaMayor.txt", "Estrellas Bonitas\constellations\OsaMenor.txt"]
    constelaciones = []
    for archivo in archivos:
        with open(archivo) as f:
            constelaciones_archivo = [tuple(line.strip().replace(" ", "").split(",")) for line in f]
        constelaciones.extend(constelaciones_archivo)
    fig, ax = plt.subplots(figsize=(8, 8))
    x_coords = [star[0] for star in stars]
    y_coords = [star[1] for star in stars]
    mag = [star[3] for star in stars]
    cmap = cm.get_cmap('Greys_r', 10)
    sizes = [3/ (m + 2) for m in mag]
    sc = ax.scatter(x_coords, y_coords, s=sizes, c=mag, cmap=cmap)
    for constelacion in constelaciones:
        estrella1, estrella2 = constelacion
        x1, y1 = next((x, y) for x, y,id, mag, nombre in stars if estrella1 in nombre)
        x2, y2 = next((x, y) for x, y,id, mag, nombre in stars if estrella2 in nombre)
        ax.plot([x1, x2], [y1, y2], '-', lw=1)
    ax.set_facecolor('black')
    sc.set_clim(0, 10)
    plt.legend()
    plt.subplots_adjust(left=0.126,
                        bottom=0.045, 
                        right=0.902, 
                        top=0.917, 
                        wspace=0.2, 
                        hspace=0.2)

    plt.title("Todas las constelaciones")
    plt.savefig(r'Estrellas Bonitas\images\todas.png')
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=r'Estrellas Bonitas\images\todas.png')


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

def limg(equation):
    """Crea una imagen como respuesta a una ecuacion en sintaxis de latex

    Args:
        equation (latex): ecuacion en sintaxis de latex para ser convertida a imagen

    Returns:
        imagen: imagen de la ecuacion convertida a latex
    """
    response = requests.get(
        'http://latex.codecogs.com/png.latex?\dpi{{1200}} {formula}'.format(formula=equation))
    imagen = BytesIO(response.content)
    return imagen


async def rrlnhccc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funcion que define el comando /rrlnhccc, el cual resuelve una relacion de recurrencia lineal no homogenea con coeficientes constantes.

    Args:
        update (Update): 
        context (ContextTypes.DEFAULT_TYPE): 
    """
    valores = update.message.text.split()[1:]
    print(valores)
    if len(valores) != 2:
        await update.message.reply_text('🥇 Digite la relacion de recurrencia no homogenea de la forma:\n\n  a*f(n-1)+b*f(n-2)+...+c*f(n-k)+g(n)\n  y despues de un espacio los valores iniciales.\n\n 🧠Por ejemplo: /rrlnhccc 4*f(n-1)-4*f(n-2)+n**2 1,3\n ')
        return
    sol= RRL.solucionar_no_homogenea(valores[0],valores[1]) 
    solucion = convertir_a_latex(sol)
    img_sol = limg(solucion)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=img_sol)


def convertir_a_latex(funcion):
    """convierte un str a sintaxis de latex

    Args:
        funcion (str): Funcion en string

    Returns:
        latex: Funcion convertida a sintaxis de latex
    """
    x = sp.sympify(funcion)
    resultado = sp.latex(x)
    return resultado

# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('starscons', starscons_command))
    app.add_handler(CommandHandler('stars', stars_command))
    app.add_handler(CommandHandler('rrlnhccc', rrlnhccc_command))
    app.add_handler(CommandHandler('todas', TODAS_command))
    app.add_handler(CommandHandler('constelacion', constelacion_command))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)