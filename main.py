import numpy as np

from lights import Light
from renderer import *
from camera import Camera
from viewport import Viewport

# Camera, screen and objects
camera = Camera([0, 0, 1], screen_size=1)
# All objects are sphere for now, but I might add support for plane and triangles later
objects = [
    {'center': np.array([0, 0, -7]), 'radius': 0.9},
    #{'center': np.array([0, -2, -4]), 'radius': 0.95},
    #{'center': np.array([0, 0, -100]), 'radius': 0.5}
]

for i in range(30):
    lights = [
        Light([0, i/10, -10 + i/10], color=(0.5, 0.5, 0.5), light_limit=5.8),
        Light([0, 0, -5], color=(1, 0.12, 0.06), light_limit=1, intensity=0.5)
    ]
    viewport = Viewport(objects, camera, lights)
    plt.imsave(f'img/image_rt{i}.png', render(viewport))
#plt.imsave('img/image_ortho.png', render_ortho_depth_map(viewport_ortho, 6, True))
#plt.imsave('img/image.png', render_depth_map(viewport, 6, True))
