from lights import Light
from material import Material
from objects import Sphere
from renderer import *
from camera import Camera
from viewport import Viewport

# Camera, screen and objects
camera = Camera([0, 0, 1], screen_size=1)
# All objects are sphere for now, but I might add support for plane and triangles later
objects = [
    Sphere([0, 0, -150], 100, Material([0.1, 0, 0], [0.7, 0, 0], [1, 1, 1], 100)),
    Sphere([0, 0, -7], 1, Material([0.1, 0, 0], [0.7, 0, 0], [1, 1, 1], 100))
]

lights = [
    Light([2, 4, -1], color=(1, 1, 1), light_limit=80, intensity=2),
    #Light([2, -2, -5], color=(1, 0.12, 0.06), light_limit=1, intensity=0.5)
]
viewport = Viewport(objects, camera, lights, height=720, width=1080)
plt.imsave(f'img/image_rt.png', render(viewport))
