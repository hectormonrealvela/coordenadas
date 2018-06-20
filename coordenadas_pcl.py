#!/usr/bin/python
# coding: utf8
import numpy
import octomap
from mayavi.mlab import *
from mayavi import mlab
from numpy import pi, sin, cos, mgrid
import numpy as np
import fcntl
import pcl
from termcolor import colored
from transforms3d.euler import euler2mat, mat2euler
import json
from getkey import getkey, keys
import ICP
import vtk

cont=0

class Viewer:
    def __init__(self):
        self.scale_factor = 0.1


        self.manejador = []
        self.ms_manejador = []
        self.scale_factor = 0.10

        self.tree = octomap.OcTree(0.20)
        print 'Default probability hit: ' + str(self.tree.getProbHit())
        print 'Default probability miss: ' + str(self.tree.getProbMiss())
        self.tree.setProbHit(0.92)
        self.tree.setProbMiss(0.40)


    def draw(self):

        cloud_source = pcl.load('/home/hector/nubedepuntos/cloud_yaw_frame_number_9.pcd')

        #Points
        points_array = cloud_source.to_array()
        self.points3d_draw = points3d(points_array[:, 0:1], points_array[:, 1:2], points_array[:, 2:3],
                                      points_array[:, 2:3], mode='sphere', scale_mode='none',
                                      scale_factor=self.scale_factor, reset_zoom=False)
        points_target = cloud_source.to_array()

        self.points3d_draw.mlab_source.reset(x=points_target[:, 0:1], y=points_target[:, 1:2], z=points_target[:, 2:3],
                                             scalars=points_target[:, 2:3])


        cursor3d = mlab.points3d(0., 0., 0., mode='sphere',
                                 color=(0, 0, 0),
                                 scale_factor=0.1)

def picker_callback( picker):

    global cont
    cont += 1

    print
    print("Coordenadas: x: %i, y: %i  , z: %i" % (picker.pick_position))
    print picker.pick_position
    print

    [x,y,z,] = picker.pick_position

    points3d(x, y, z, color=(0, 0, 0), scale_factor=0.1, mode='sphere', scale_mode='none', reset_zoom=False)

    with open('Bbdd_Frame_9.doc',"a") as file:
        file.write(" BBdd Frame 9 Objeto num: %i  "%(cont))
        file.write("Coordenada x: %i, Coordenada y: %i, Coordenada z: %i\n\n" %(picker.pick_position))
        file.close()

viewer = Viewer()
viewer.draw()
fig= mlab.figure(1)
fig.on_mouse_pick(picker_callback,type='world')
show()
