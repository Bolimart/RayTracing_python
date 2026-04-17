import numpy as np


class Material:

    def __init__(self, ambient, diffuse, specular=np.array([1, 1, 1]), shininess=100):
        self.shininess = shininess
        self.specular = specular
        self.diffuse = diffuse
        self.ambient = ambient

