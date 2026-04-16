import numpy as np
import matplotlib.pyplot as plt
from viewport import Viewport


# ----[ UTILITIES ]----


def normalize(vector):
    # Vector / length of the vector
    return vector / np.linalg.norm(vector)


def set_unicolor(x, y, image, color):
    image[x, y, 0] = color
    image[x, y, 1] = color
    image[x, y, 2] = color


def set_color(x, y, image, color):
    image[x, y, 0] = max(0, min(color[0], 1))
    image[x, y, 1] = max(0, min(color[1], 1))
    image[x, y, 2] = max(0, min(color[2], 1))


# ----[ INTERSECTION FUNCTIONS ]----


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


def get_pixel_color(viewport: Viewport, ray_origin, ray_direction):

    nearest_object, min_dist = nearest_intersect_object(viewport.objects, ray_origin, ray_direction)
    color = (0, 0, 0)

    if nearest_object is None:
        return 0, 0, 0

    intersection = ray_origin + ray_direction * min_dist
    normal = normalize(intersection - nearest_object["center"])
    shifted_point = intersection + 1e-5 * normal  # We slightly shift the point to avoid the sphere from coliding with itself

    for light in viewport.lights:
        direction_to_light = normalize(light.pos - intersection)

        obs, obs_dist = nearest_intersect_object(viewport.objects, shifted_point, direction_to_light)
        light_dist = np.linalg.norm(light.pos - intersection)
        is_shadowed = min_dist < light_dist
        if not is_shadowed:  # Might add emmisive materials later.
            color = light.get_light_amount(light_dist)
        else:
            if obs is not None:
                print(obs["id"])

    return color


# ----[ RENDER FUNCTIONS ]----


def render_depth_map(viewport: Viewport, view_dist, debug=False):
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
            set_unicolor(i, j, image, 1 - min(dist, 1))

        if debug:
            print(f"progress: {(i + 1) * 100 // viewport.height}%")

    return image


def render_ortho_depth_map(viewport: Viewport, view_dist, debug=False):
    # Create the empty image array, with an image depth of three (R, G and B)
    image = np.zeros((viewport.height, viewport.width, 3))
    v, h = viewport.camera.make_pos_array(viewport.height, viewport.width)
    # For each pixel of the image:
    for i, y in enumerate(v):
        for j, x in enumerate(h):
            pixel = np.array([x, y, 0])  # D (for destination) | z = 0 since the camera is on the x, y plane | Might add tilted camera support later
            direction = np.array([0, 0, -1])  # d = D - O / || D - O || (for direction

            dist = nearest_intersect_object(viewport.objects, pixel, direction)[1] / view_dist
            set_unicolor(i, j, image, 1 - min(dist, 1))

        if debug:
            print(f"progress: {(i + 1) * 100 // viewport.height}%")

    return image


def render(viewport, iteration=0, debug=False):
    # Create the empty image array, with an image depth of three (R, G and B)
    image = np.zeros((viewport.height, viewport.width, 3))
    v, h = viewport.camera.make_pos_array(viewport.height, viewport.width)
    # For each pixel of the image:
    for i, y in enumerate(v):
        for j, x in enumerate(h):
            pixel = np.array([x, y, 0])  # D (for destination) | z = 0 since the camera is on the x, y plane | Might add tilted camera support later
            origin = viewport.camera.pos  # O (for origin
            direction = normalize(pixel - origin)  # d = D - O / || D - O || (for direction)

            color = get_pixel_color(viewport, origin, direction)
            set_color(i, j, image, color)

        if debug:
            print(f"progress: {(i + 1) * 100 // viewport.height}%")

    return image
