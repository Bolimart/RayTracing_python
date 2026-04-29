from lights import Light
from material import Material
import numpy as np


def normalize(vector):
    # Vector / length of the vector
    return vector / np.linalg.norm(vector)


class RenderObject:

    def __init__(self, pos, material: Material):
        self.pos = pos
        self.material = material


    def intersect(self, ray_origin, ray_direction):
        pass


    def normal(self, intersection):
        return [0, 0, 0]


    def BP_ilumination_point(self, light: Light, camera, intersection, normal_to_surface, intersection_to_light):

        ambiant = self.material.ambient * light.material.ambient
        diffuse = self.material.diffuse * light.material.diffuse * np.dot(intersection_to_light, normal_to_surface)
        intersection_to_camera = normalize(camera.pos - intersection)
        H = normalize(intersection_to_light + intersection_to_camera)
        specular = self.material.specular * light.material.specular * max(np.dot(normal_to_surface, H), 0) ** self.material.shininess

        illumination = np.zeros(3) + ambiant + diffuse + (specular * self.material.shininess / 100)
        return illumination



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


    def normal(self, intersection):
        return normalize(intersection - self.pos)
