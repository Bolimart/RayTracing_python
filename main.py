import numpy as np

from lights import Light
from renderer import *
from camera import Camera
from viewport import Viewport

# Camera, screen and objects
camera = Camera([0, 0, 1], screen_size=1)
# All objects are sphere for now, but I might add support for plane and triangles later
objects = [
    #{'center': np.array([-2, 1, -6]), 'radius': 0.9},
    {'center': np.array([0, 0, -10]), 'radius': 0.99, 'id': "projector"},
    {'center': np.array([0, 0, -100]), 'radius': 0.5, 'id': "screen"}
]
lights = [
    Light([6, 0, -1], color=(1, 1, 1), light_limit=30)
]
viewport = Viewport(objects, camera, lights)
plt.imsave(f'img/image_rt.png', render(viewport))

# for i in range(-10, 10):
#     lights = [
#         Light([i/5, 0, -1], color=(1, 1, 1), light_limit=30)
#     ]
#     viewport = Viewport(objects, camera, lights)
#     plt.imsave(f'img/image_rt_h{i}.png', render(viewport))
#plt.imsave('img/image_ortho.png', render_ortho_depth_map(viewport_ortho, 6, True))
#plt.imsave('img/image.png', render_depth_map(viewport, 6, True))
