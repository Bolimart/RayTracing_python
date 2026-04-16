from camera import Camera


class Viewport:

    def __init__(self, objects, camera: Camera, width=300, height=200):
        self.objects = objects
        self.camera = camera
        self.width = width
        self.height = height

        self.ratio = float(width) / height
        self.camera.make_screen(self.ratio)
