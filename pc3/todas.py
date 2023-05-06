import matplotlib.pyplot as plt


with open("stars.txt", 'r') as f:
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

archivos = ["constellations/Boyero.txt", "constellations/Casiopea.txt", 
            "constellations/Cazo.txt", "constellations/Cygnet.txt","constellations/Geminis.txt",
            "constellations/Hydra.txt", "constellations/OsaMayor.txt", "constellations/OsaMenor.txt"]
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
plt.show()