import numpy as np
import math
from utils import *

#------------------ Camera ------------------

class Camera():
    def __init__(self, engine, x, y, z):
        self.eng = engine
        self.position = np.array([x,y,z, 1.0])

        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

        self.near = 0.1
        self.far = 100
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (engine.height / engine.width)
        self.flen = 1/(math.tan(self.h_fov/2))
        self.aspectR = engine.width/engine.height

        self.moving_speed = 0.3

    def movement(self, key):
        # horizontal movement
        if key == ord('a'):
            self.position -= self.right * self.moving_speed
        if key == ord('d'):
            self.position += self.right * self.moving_speed
        
        # vertical movement
        if key == ord('w'):
            self.position += self.forward * self.moving_speed
        if key == ord('s'):
            self.position -= self.forward * self.moving_speed
        
        # depth movement
        if key == ord('q'):
            self.position += self.up * self.moving_speed
        if key == ord('e'):
            self.position -= self.up * self.moving_speed

        # y axis rotation
        if key == ord('z'):   
            self.rotate('y', -self.moving_speed)
        if key == ord('x'):   
            self.rotate('y', self.moving_speed)
        
        # x axis rotation
        if key == ord('m'):  
            self.rotate('x', -self.moving_speed)
        if key == ord('n'):   
            self.rotate('x', self.moving_speed)

        # z axis rotation
        if key == ord('o'):  
            self.rotate('z', -self.moving_speed)
        if key == ord('p'):   
            self.rotate('z', self.moving_speed)

    def rotate(self, axis, angle):
        if axis == 'x':
            R = rotate_x(angle)
        elif axis == 'y':
            R = rotate_y(angle)
        elif axis == 'z':
            R = rotate_z(angle)
        else:
            return

        self.forward =  self.forward @ R 
        self.up = self.up @ R 
        self.right = self.right @ R 

    #Convert to camera coordinates
    def camMat(self):
        x,y,z,w = self.position
        
        translate = np.array([
            [1,0,0,0],
            [0,1,0,1],
            [0,0,1,0],
            [-x,-y,-z,1]
        ])


        fx, fy, fz, fw = self.forward
        ux, uy, uz, uw = self.up
        rx, ry, rz, rw = self.right
        
        rotate = np.array([
            [rx,ux,fx,0],
            [ry,uy,fy,0],
            [rz,uz,fz,0],
            [0,0,0,1]
        ])


        return translate @ rotate

    # openGl projection matrix -  view volume is between -1 and 1 on all 3 axes
    # left hand coordinate system
    def projectMat(self):
        p = np.array([
            [self.flen/self.aspectR,0,0,0],
            [0,self.flen,0,0],
            [0,0,(self.far+self.near)/(self.far - self.near),1],
            [0,0,-2*self.far*self.near/(self.far - self.near),0]
        ])
        return p


    def screenMat(self):
        hw = self.eng.width/2
        hh = self.eng.height/2
        m = np.array([
            [hw,0,0,0],
            [0,hh,0,0],
            [0,0,1,0],
            [hw,hh,0,1]
        ])
        return m