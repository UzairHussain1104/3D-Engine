import cv2
import numpy as np
from camera import Camera
from object import Object


""" 
WASD keys to move forwards and back
QE for up and down
ZX for rotation around y axis
NM for rotation around x axis
OP for rotatio around z axis
"""

#---------- Cube faces and vertices ----------

verts = np.array([
    [0,0,0,1],
    [0,1,0,1],
    [1,1,0,1],
    [1,0,0,1],
    [0,0,1,1],
    [0,1,1,1],
    [1,1,1,1],
    [1,0,1,1],
])


faces = np.array([
    [0,1,2,3],
    [4,5,6,7],
    [0,5,6,7],
    [2,3,7,6],
    [1,2,6,5],
    [0,3,7,4],
])


#------------------ Engine ------------------

class Engine():
    def __init__(self, verts, faces, x, y, z):
        self.width = 800
        self.height = 600
        self.cam = Camera(self, x, y, z)
        self.object = Object(self, verts, faces)


    def NDC(self):
        return self.object.NDC()


    def run(self):
        while True:
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

            verts = self.NDC()
            verts = verts @ self.cam.screenMat()
            verts = verts[:, :2]

            for face in self.object.faces:
                poly = verts[face]
                if np.isnan(poly).any():
                    continue
                poly = poly[:, :2].astype(int)
                cv2.polylines(frame, [poly], isClosed=True, color=(255,255,255), thickness=1)


            cv2.imshow("3D Cube", frame)
            key = cv2.waitKey(30) & 0xFF
            
            if key == 27: # ESC to quit
                break
            
            self.cam.movement(key)


        cv2.destroyAllWindows()


render = Engine(verts, faces, 0.5, 0.5, -6)
render.run()