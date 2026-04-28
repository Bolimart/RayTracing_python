import numpy as np


class Material:

    def __init__(self, ambient, diffuse, specular=np.array([1, 1, 1]), shininess=100, reflection=0.5):
        self.shininess = shininess
        self.specular = np.array(specular)
        self.diffuse = np.array(diffuse)
        self.ambient = np.array(ambient)
        self.reflection = reflection

