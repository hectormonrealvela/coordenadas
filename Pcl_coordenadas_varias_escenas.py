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
from mayavi.core.ui.api import MlabSceneModel
from tvtk.pyface.scene_editor import SceneEditor
from traits.api import HasTraits, Instance, Button, on_trait_change
from traitsui.api import View, Item, HSplit, Group



cont = -1
cont2 = 0



lista =['/home/hector/PycharmProjects/mayavi/mapas/cloud_yaw_frame_number_0.pcd',
            '/home/hector/PycharmProjects/mayavi/mapas/cloud_yaw_frame_number_1.pcd',
            '/home/hector/PycharmProjects/mayavi/mapas/cloud_yaw_frame_number_2.pcd',
            '/home/hector/PycharmProjects/mayavi/mapas/cloud_yaw_frame_number_3.pcd',
            '/home/hector/PycharmProjects/mayavi/mapas/cloud_yaw_frame_number_4.pcd',
            '/home/hector/PycharmProjects/mayavi/mapas/cloud_yaw_frame_number_5.pcd',
            '/home/hector/PycharmProjects/mayavi/mapas/cloud_yaw_frame_number_6.pcd',
            ]



class MyDialog(HasTraits):


    scale_factor = 0.10
    manejador = []
    ms_manejador = []
    scene2 = Instance(MlabSceneModel, ())


    def picker_callback(self,picker):
        global cont2
        cont2 +=1
        print
        print("Coordenadas: x: %.2f, y: %.2f  , z: %.2f" % (picker.pick_position))
        print picker.pick_position
        print

        [x, y, z, ] = picker.pick_position

        points3d(x, y, z, color=(0, 0, 0), scale_factor=0.1, mode='sphere', scale_mode='none', reset_zoom=False)

        with open('Bbdd_CLoud.doc', "a") as file:
            file.write(" BBdd Frame: %i Objeto num: %i  " % (cont,cont2))
            file.write("Coordenada x: %.2f, Coordenada y: %.2f, Coordenada z: %.2f\n\n" % (picker.pick_position))
            file.close()

    button1 = Button('limpiar pantalla')
    button2 = Button('Siguiente')
    button3 = Button('Anterior')


    @on_trait_change('scene2.activated')
    def picker_active(self):
        picker = self.scene2.mayavi_scene.on_mouse_pick(self.picker_callback, type='world')


    @on_trait_change('button1')
    def clear_figure(self):
        for child in self.scene2.mayavi_scene.children:
            child.remove()
            
        for child in self.scene2.mayavi_scene.children:
           child.remove()
    


    @on_trait_change('button2')
    def siguiente(self):
        global cont
        cont += 1

        print ("Actualmente se esta representando Cloud_yaw_frame_number_ %i"%(cont))

        cloud_source = pcl.load(lista[cont])
        points_array = cloud_source.to_array()

        self.points3d_draw = points3d(points_array[:, 0:1], points_array[:, 1:2], points_array[:, 2:3],
                                      points_array[:, 2:3], mode='sphere', scale_mode='none',
                                      scale_factor=self.scale_factor, reset_zoom=False, figure=self.scene2.mayavi_scene)

        points_target = cloud_source.to_array()
        self.points3d_draw.mlab_source.reset(x=points_target[:, 0:1], y=points_target[:, 1:2], z=points_target[:, 2:3],
                                             scalars=points_target[:, 2:3], figure=self.scene2.mayavi_scene)

        cursor3d = mlab.points3d(0., 0., 0., mode='sphere',
                                 color=(0, 0, 0),
                                 scale_factor=0.1)

    @on_trait_change('button3')
    def anterior(self):
        global cont
        cont -= 1
        print ("Actualmente se esta representando Cloud_yaw_frame_number_ %i" % (cont))

        cloud_source = pcl.load(lista[cont])
        points_array = cloud_source.to_array()

        self.points3d_draw = points3d(points_array[:, 0:1], points_array[:, 1:2], points_array[:, 2:3],
                                          points_array[:, 2:3], mode='sphere', scale_mode='none',
                                          scale_factor=self.scale_factor, reset_zoom=False,
                                          figure=self.scene2.mayavi_scene)

        points_target = cloud_source.to_array()
        self.points3d_draw.mlab_source.reset(x=points_target[:, 0:1], y=points_target[:, 1:2],
                                                 z=points_target[:, 2:3],
                                                 scalars=points_target[:, 2:3], figure=self.scene2.mayavi_scene)

        cursor3d = mlab.points3d(0., 0., 0., mode='sphere',
                                     color=(0, 0, 0),
                                     scale_factor=0.1)

        # The layout of the dialog created
    view = View(HSplit(

                  Group(
                       Item('scene2',
                            editor=SceneEditor(), height=250,
                            width=300, show_label=False),
                       'button2','button1','button3',
                       show_labels=False,
                  ),

                ),
                resizable=True,
                )
if __name__ == '__main__':
    m = MyDialog()
    m.configure_traits()
