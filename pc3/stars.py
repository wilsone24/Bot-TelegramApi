import matplotlib.pyplot as plt

stars = []
with open("stars.txt") as file:
    for line in file:
        data = line.strip().split()
        x, y, _, id, mag, harvard, *name = data[:7]
        stars.append((float(x), float(y), id, float(mag), harvard, name if isinstance(name, list) else name.split(" ")))

x_coords = [star[0] for star in stars]
y_coords = [star[1] for star in stars]
plt.scatter(x_coords, y_coords, s=5)
plt.subplots_adjust(left=0.148,
                    bottom=0.062, 
                    right=0.86, 
                    top=1, 
                    wspace=0.2, 
                    hspace=0.2)
plt.title("Todas las estrellas")
plt.show()