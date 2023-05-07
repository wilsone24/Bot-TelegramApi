
import matplotlib.pyplot as plt

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


constelaciones = ['Boyero', 'Casiopea', 'Cazo', 'Cygnet', 'Geminis', 'Hydra', 'OsaMayor', 'OsaMenor']

# Pedir al usuario que seleccione una constelación
print("Seleccione una constelación para graficar:")
for i, constelacion in enumerate(constelaciones):
    print(f"{i+1}. {constelacion}")
opcion = int(input("Opción: "))


with open(f'Bot-TelegramApi\Constellations\constellations\{constelaciones[opcion-1]}.txt') as f:
    constelaciones_archivo = [tuple(line.strip().replace(" ", "").split(",")) for line in f]


fig, ax = plt.subplots()
for estrella in stars:
    x, y = estrella[0], estrella[1]
    ax.scatter(x, y,s=5)

for constelacion in constelaciones_archivo:
    estrella1, estrella2 = constelacion
    x1, y1 = next((x, y) for x, y, nombre in stars if estrella1 in nombre)
    x2, y2 = next((x, y) for x, y, nombre in stars if estrella2 in nombre)
    ax.plot([x1, x2], [y1, y2], '-', lw=1.5)

ax.legend()
plt.subplots_adjust(left=0.148,
                    bottom=0.062, 
                    right=0.86, 
                    top=1, 
                    wspace=0.2, 
                    hspace=0.2)
plt.grid(lw=0.2)
plt.show() 