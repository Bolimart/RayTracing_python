import numpy as np


class Camera:

    def __init__(self, pos, screen_pos=(0, 0), screen_size=1):
        self.pos = np.array(pos)
        self.screen_pos = screen_pos    # The pos of the screen relative to the camera
        self.screen_size = screen_size
        self.screen = (0, 0, 0, 0)


    def make_screen(self, ratio):
        a = -self.screen_size - self.screen_pos[0]
        b = self.screen_size/ratio + self.screen_pos[1]
        c = self.screen_size - self.screen_pos[0]
        d = -self.screen_size/ratio + self.screen_pos[1]
        self.screen = (a, b, c, d)


    def make_pos_array(self, height, width):
        v = np.linspace(self.screen[1], self.screen[3], height)  # Take the vertical pos of each pixel (eg: linspace(-1, 1, 4) -> [-1., -0.33,  0.33,  1.])
        h = np.linspace(self.screen[0], self.screen[2], width)   # Take the horizontal pos of each pixel
        return v, h
