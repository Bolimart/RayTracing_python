import numpy as np


class Material:

    def __init__(self, ambient, diffuse, specular, shininess):
        self.shininess = shininess
        self.specular = specular
        self.diffuse = diffuse
        self.ambient = ambient
