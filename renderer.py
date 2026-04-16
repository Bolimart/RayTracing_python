import numpy as np
import matplotlib.pyplot as plt
from camera import Camera
from viewport import Viewport

# Resolution of the screen
view_dist = 6


def set_color(x, y, image, color):
    image[x, y, 0] = color
    image[x, y, 1] = color
    image[x, y, 2] = color


def nearest_intersect_object(objects, ray_origin, ray_direction):
    # Return the min distance and nearest object of the ray
    distances = [sphere_intersection(obj["center"], obj["radius"], ray_origin, ray_direction) for obj in objects]
    nearest_object = None
    min_dist = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_dist:
            min_dist = distance
            nearest_object = objects[index]
    return nearest_object, min_dist


def normalize(vector):
    # Vector / length of the vector
    return vector / np.linalg.norm(vector)


def sphere_intersection(center, radius, ray_origin, ray_direction):
    # Sphere equation   -   ||X - C||² = r²
    # Sphere intersection - ||O + d * t - C||² = r²                             ||X||² = dot(X, X)  a = ||d||² = 1
    #                       dot(O + d * t - C, O + d * t - C) = r²                                  b = 2*dot(d, O - C)
    #                       ||d, d||²t² + 2t*dot(d, O - C) + ||O - C||² * r² = 0                    c = ||O - C||² * r²
    # We search for the delta (b² - 4ac) when it is superior to 0, then we search for the nearest solution of E
    b = 2 * np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center)**2 * radius**2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:  # Avoid clipping
            return min(t1, t2)
    return None


# Camera, screen and objects
camera = Camera([0, 0, 1])
# All objects are sphere for now, but I might add support for plane and triangles later
objects = [
    {'center': np.array([-2, 1, -6]), 'radius': 0.9},
    {'center': np.array([-0.4, -1, -3.5]), 'radius': 0.95},
    {'center': np.array([1.8, -0.5, -7]), 'radius': 0.85}
]
viewport = Viewport(objects, camera)


def render(viewport: Viewport):
    # Create the empty image array, with an image depth of three (R, G and B)
    image = np.zeros((viewport.height, viewport.width, 3))
    v, h = viewport.camera.make_pos_array(viewport.height, viewport.width)
    # For each pixel of the image:
    for i, y in enumerate(v):
        for j, x in enumerate(h):
            pixel = np.array([x, y, 0])   # D (for destination) | z = 0 since the camera is on the x, y plane | Might add tilted camera support later
            origin = viewport.camera.pos  # O (for origin
            direction = normalize(pixel - origin)  # d = D - O / || D - O || (for direction)

            dist = nearest_intersect_object(viewport.objects, origin, direction)[1] / view_dist
            set_color(i, j, image, 1 - min(dist, 1))

        # print(f"progress: {(i + 1) * 100 // viewport.height}%")
    return image
