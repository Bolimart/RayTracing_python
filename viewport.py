from camera import Camera
from lights import Light


class Viewport:

    def __init__(self, objects, camera: Camera, lights: list[Light],  width=300, height=200):
        self.objects = objects
        self.lights = lights
        self.camera = camera
        self.width = width
        self.height = height

        self.ratio = float(width) / height
        self.camera.make_screen(self.ratio)
