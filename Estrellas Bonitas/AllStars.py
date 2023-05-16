import matplotlib.pyplot as plt
import matplotlib.cm as cm

stars = []
with open('stars.txt') as file:
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
plt.show()


