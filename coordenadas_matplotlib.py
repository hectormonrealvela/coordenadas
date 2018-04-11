###########   Librerias

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from mpldatacursor import datacursor


fig = plt.figure()
ax =Axes3D(fig)

###########  Datos figura 3d

X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)
plt.axis("off")


#### Nos da las coordenadas

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
datacursor(surf)

####### Muestra la figura

plt.show()
