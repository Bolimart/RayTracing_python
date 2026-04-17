import numpy as np
from objects import RenderObject
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
    image[x, y] = np.clip(color, 0, 1)


# ----[ INTERSECTION FUNCTIONS ]----


def nearest_intersect_object(objects: list[RenderObject], ray_origin, ray_direction):
    # Return the min distance and nearest object of the ray
    distances = [obj.intersect(ray_origin, ray_direction) for obj in objects]
    nearest_object = None
    min_dist = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_dist:
            min_dist = distance
            nearest_object = objects[index]
    return nearest_object, min_dist


def get_pixel_color(viewport: Viewport, ray_origin, ray_direction):

    nearest_object, min_dist = nearest_intersect_object(viewport.objects, ray_origin, ray_direction)
    color = [0, 0, 0]

    if nearest_object is None:
        return 0, 0, 0

    for light in viewport.lights:
        intersection = ray_origin + min_dist * ray_direction

        normal_to_surface = nearest_object.normal(intersection)
        shifted_point = intersection + (1e-5 * normal_to_surface)  # if there is strange self shadowing, raducing 1e-5 might help
        intersection_to_light = normalize(light.pos - shifted_point)

        _, min_distance = nearest_intersect_object(viewport.objects, shifted_point, intersection_to_light)
        intersection_to_light_distance = np.linalg.norm(light.pos - intersection)
        is_shadowed = min_distance < intersection_to_light_distance

        if is_shadowed:
            continue
        else:
            illumination = nearest_object.BP_ilumination_point(light, viewport.camera, intersection, normal_to_surface, intersection_to_light)
            color += np.clip(illumination, 0, 1)

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
