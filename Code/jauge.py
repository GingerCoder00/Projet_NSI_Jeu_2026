import matplotlib.pyplot as plt

serie1 = [7, 6, 5, 7, 6, 5, 8]
serie2 = [1, 0, 2, 0, 1, 1, 2]
plt.bar(range(0,7), serie1)
plt.bar(range(0,7), serie2, bottom=serie1)
plt.show()

#pollution, humidité
#change de couleur en fonction du niveau