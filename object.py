import numpy as np

# ------------------ Object ------------------

class Object():
    def __init__(self, engine, vertices, faces):
        self.verts = vertices
        self.faces = faces
        self.eng = engine


    def NDC(self):
        verts = self.verts @ self.eng.cam.camMat()
        verts = verts @ self.eng.cam.projectMat()
        
        # Clip vertices behind camera (z <= 0 in camera space)
        in_front = verts[:, 2] > 0
        verts[~in_front] = np.nan  # mark behind-camera points as NaN
        
        verts /= verts[:, -1].reshape(-1, 1)
        
        
        return verts