
import matplotlib.pyplot as plt
import matplotlib.cm as cm

with open('stars.txt', 'r') as f:
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


archivos = ["constellations\Boyero.txt", "constellations\Casiopea.txt", 
            "constellations\Cazo.txt", "constellations\Cygnet.txt","constellations\Geminis.txt",
            "constellations\Hydra.txt", "constellations\OsaMayor.txt", "constellations\OsaMenor.txt"]


constelaciones = ['Boyero', 'Casiopea', 'Cazo', 'Cygnet', 'Geminis', 'Hydra', 'OsaMayor', 'OsaMenor']

# Pedir al usuario que seleccione una constelación
print("Seleccione una constelación para graficar:")
for i, constelacion in enumerate(constelaciones):
    print(f"{i+1}. {constelacion}")
opcion = int(input("Opción: "))


with open(f'constellations\{constelaciones[opcion-1]}.txt') as f:
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
plt.show()