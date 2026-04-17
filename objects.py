from material import Material
import numpy as np


class RenderObject:

    def __init__(self, pos, material: Material):
        self.pos = pos
        self.material = material


    def intersect(self, ray_origin, ray_direction):
        pass


class Sphere(RenderObject):

    def __init__(self, center, radius, material: Material):
        super().__init__(center, material)
        self.radius = radius


    def intersect(self, ray_origin, ray_direction):
        # Sphere equation   -   ||X - C||² = r²
        # Sphere intersection - ||O + d * t - C||² = r²                             ||X||² = dot(X, X)  a = ||d||² = 1
        #                       dot(O + d * t - C, O + d * t - C) = r²                                  b = 2*dot(d, O - C)
        #                       ||d, d||²t² + 2t*dot(d, O - C) + ||O - C||² * r² = 0                    c = ||O - C||² * r²
        # We search for the delta (b² - 4ac) when it is superior to 0, then we search for the nearest solution of E
        b = 2 * np.dot(ray_direction, ray_origin - self.pos)
        c = np.linalg.norm(ray_origin - self.pos) ** 2 - self.radius ** 2
        delta = b ** 2 - 4 * c
        if delta > 0:
            t1 = (-b + np.sqrt(delta)) / 2
            t2 = (-b - np.sqrt(delta)) / 2
            if t1 > 0 and t2 > 0:
                return min(t1, t2)
        return None
