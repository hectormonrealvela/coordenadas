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
import vtk
import json

from mayavi.core.ui.api import MlabSceneModel
from tvtk.pyface.scene_editor import SceneEditor
from traits.api import HasTraits, Instance, Button, on_trait_change
from traitsui.api import View, Item, HSplit, Group




class MyDialog(HasTraits):
    scene2 = Instance(MlabSceneModel, ())
    scale_factor = 0.10
    points_picked = []
    count = 0
    point_cloud_number = 0
    cont = 134
    cont2 = 0

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

    def picker_callback(self,picker):
        self.cont2 +=1
        print
        print("Coordenadas: x: %.2f, y: %.2f  , z: %.2f" % (picker.pick_position))
        print picker.pick_position
        print

        [x, y, z, ] = picker.pick_position

        self.scene2.mlab.points3d(x, y, z, color=(0, 0, 0), scale_factor=0.05, mode='sphere', scale_mode='none', reset_zoom=False, figure=self.scene2.mayavi_scene)

        with open('Bbdd_CLoud.doc', "a") as file:
            file.write(" BBdd Frame: %i Objeto num: %i  " % (self.cont,self.cont2))
            file.write("Coordenada x: %.2f, Coordenada y: %.2f, Coordenada z: %.2f\n\n" % (picker.pick_position))
            file.close()

    button1 = Button('limpiar pantalla')
    button2 = Button('Siguiente')
    button3 = Button('Anterior')

    def picker_callback_2(self, picker):
      scale_factor = 0.05

      if self.count == 0: print 'Point I'
      elif self.count == 1: print 'Point J'
      elif self.count == 2: print 'Point M'
      elif self.count == 3: print  'Point L'

      self.points_picked.append(picker.pick_position)
      if self.count == 3:
          self.count = -1
          data = {'cloud_number:': self.cont+1, 'i': self.points_picked[0], 'j': self.points_picked[1], 'l': self.points_picked[2], 'm': self.points_picked[3]}
          print data
          print 'Is the point collection correct? (y/n)'
          key = getkey()
          if key == 'y':
              print 'The result has been copied to file.'
              self.file_p = open('bbdd.dat', 'a')
              self.file_p.write(json.dumps(data))
              self.file_p.write('\n')
              self.file_p.close()
          else:
              print 'The point collection is not correct.'


          self.points_picked = []


      self.count += 1

      [x,y,z] = picker.pick_position
      points3d(x, y, z, color=(0, 0, 0), scale_factor=scale_factor, mode='sphere', scale_mode='none', reset_zoom=False)



    @on_trait_change('scene2.activated')
    def picker_active(self):
        picker = self.scene2.mayavi_scene.on_mouse_pick(self.picker_callback_2, type='world', button='Right')



    @on_trait_change('button1')
    def clear_figure(self):
        p=0
        while p<4:
         for child in self.scene2.mayavi_scene.children:
            child.remove()

         p+=1


    @on_trait_change('button2')
    def siguiente(self):

        self.cont += 1

        print ("Actualmente se esta representando Cloud_yaw_frame_number_" + str(self.cont+1) +" y Cloud_yaw_frame_number_" + str(self.cont))

        cloud_source = pcl.load('../clouds_test_v3/cloud_yaw_frame_number_1.pcd')
        points_array = cloud_source.to_array()

        self.points3d_draw = points3d(points_array[:, 0:1], points_array[:, 1:2], points_array[:, 2:3],
                                      points_array[:, 2:3], mode='sphere', scale_mode='none',
                                      scale_factor=self.scale_factor, reset_zoom=False, figure=self.scene2.mayavi_scene)

        cloud_source = pcl.load('../clouds_test_v3/cloud_yaw_frame_number_' + str(self.cont) + '.pcd')
        points_array = cloud_source.to_array()

        self.points3d_draw = points3d(points_array[:,0], points_array[:,1], points_array[:,2],
                                      color=(1,1,1), mode='sphere', scale_mode='none',
                                      scale_factor=self.scale_factor, reset_zoom=False, figure=self.scene2.mayavi_scene)

    @on_trait_change('button3')
    def anterior(self):

        self.cont -= 1

        print ("Actualmente se esta representando Cloud_yaw_frame_number_" + str(self.cont+1) +" y Cloud_yaw_frame_number_" + str(self.cont))

        cloud_source = pcl.load('../clouds_test_v3/cloud_yaw_frame_number_' + str(self.cont+1) + '.pcd')
        points_array = cloud_source.to_array()

        self.points3d_draw = points3d(points_array[:, 0:1], points_array[:, 1:2], points_array[:, 2:3],
                                          points_array[:, 2:3], mode='sphere', scale_mode='none',
                                          scale_factor=self.scale_factor, reset_zoom=False,
                                          figure=self.scene2.mayavi_scene)

        cloud_source = pcl.load('../clouds_test_v3/cloud_yaw_frame_number_' + str(self.cont) + '.pcd')
        points_array = cloud_source.to_array()

        self.points3d_draw = points3d(points_array[:, 0], points_array[:, 1], points_array[:, 2],
                                      color=(1, 1, 1), mode='sphere', scale_mode='none',
                                      scale_factor=self.scale_factor, reset_zoom=False, figure=self.scene2.mayavi_scene)


if __name__ == '__main__':
    m = MyDialog()
    m.configure_traits()
