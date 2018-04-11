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
cursor3d = mlab.points3d(0., 0., 0., mode='axes',
                                color=(0, 0, 0),
                                scale_factor=0.1)
mlab.view(45, 0)

###### Funcion con la que el programa nos muestra en pantalla el valor de x e y #####

def picker_callback(picker_obj):
    import numpy as np
    picked = picker_obj.actors
    if mesh.actor.actor._vtk_obj in [o._vtk_obj for o in picked]:
        x_, y_ = np.lib.index_tricks.unravel_index(picker_obj.point_id,
                                                   S.shape)
        print("Coordenadas: x: %i, y: %i  " % (x_, y_,))
        n_x, n_y, = S.shape

        cursor3d.mlab_source.reset(x=X[x_, y_],
                                   y=Y[x_, y_],
                                   z=Z[x_, y_])

#llamamos a dicha funcion

fig.on_mouse_pick(picker_callback)

# Nos muestra la figura

mlab.show()
