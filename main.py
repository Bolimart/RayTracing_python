import numpy as np

from lights import Light
from material import Material
from objects import Sphere
from renderer import *
from camera import Camera
from viewport import Viewport
import matplotlib.pyplot as plt

# Camera, screen and objects
camera = Camera([0, 0, 1], screen_size=1)
# All objects are sphere for now, but I might add support for plane and triangles later
objects = [
    Sphere(np.array([0.8, 0, -1]), 0.7, Material( np.array([0.1, 0, 0]), np.array([0.7, 0, 0]), np.array([1, 1, 1]), 100)),
    Sphere(np.array([-0.8, 0, -2]), 1.4, Material( np.array([0, 0, 0.1]), np.array([0, 0, 0.7]), np.array([1, 1, 1]), 60)),
    Sphere(np.array([0.3, 0.3, -0.15]), 0.1, Material([0.1, 0, 0.1], [0.7, 0, 0.7], [1, 1, 1], 50)),
    Sphere(np.array([-0.3, -0.10, 0]), 0.25, Material([0, 0.1, 0], [0, 0.6, 0], [1, 1, 1], 0))
]

lights = [
    Light(np.array([5, 5, 5]), material=Material(np.array([1, 1, 1]), np.array([1, 1, 1]) ), light_limit=80, intensity=2),
    #Light(np.array([-5, -5, 5]), material=Material(np.array([0.6, .1, 0.1]), np.array([0.6, 0.1, 0.1]), np.array([0.1, 0.1, 0.1])), light_limit=80, intensity=0.5),
    #Light(np.array([5, -5, 5]), material=Material(np.array([0.1, .1, 0.6]), np.array([0.1, 0.1, 0.6]), np.array([0.1, 0.1, 0.1])), light_limit=80, intensity=0.5),
    #Light([2, -2, -5], color=(1, 0.12, 0.06), light_limit=1, intensity=0.5)
]
viewport = Viewport(objects, camera, lights, height=720, width=1080)
plt.imsave(f'img/image_rt.png', render(viewport, debug=True))
