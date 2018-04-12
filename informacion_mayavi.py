#Librerias que utilizamos

from numpy import sin, cos, mgrid, pi, sqrt
from mayavi import mlab

# datos del dibujo de la figura de Mayavi

mlab.figure(fgcolor=(0, 0, 0), bgcolor=(1, 1, 1))
u, v = mgrid[- 0.035:pi:0.01, - 0.035:pi:0.01]

X = 2 / 3. * (cos(u) * cos(2 * v)
        + sqrt(2) * sin(u) * cos(v)) * cos(u) / (sqrt(2) -
                                                 sin(2 * u) * sin(3 * v))
Y = 2 / 3. * (cos(u) * sin(2 * v) -
        sqrt(2) * sin(u) * sin(v)) * cos(u) / (sqrt(2)
        - sin(2 * u) * sin(3 * v))
Z = -sqrt(2) * cos(u) * cos(u) / (sqrt(2) - sin(2 * u) * sin(3 * v))
S = sin(u)

mlab.mesh(X, Y, Z, scalars=S, colormap='YlGnBu', )

############ Comandos para generar el cursor ###########

fig = mlab.figure(1)
mlab.clf()
mesh = mlab.mesh(X, Y, Z, scalars=S)

mlab.view(45, 0)

###### Funcion con la que el programa nos muestra en pantalla el valor de x e y #####

def picker_callback(picker_obj):
    import numpy as np
    print(picker_obj)
    print
    print

#llamamos a dicha funcion

fig.on_mouse_pick(picker_callback)

# Nos muestra la figura

mlab.show()

