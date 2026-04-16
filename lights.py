

class Light:

    def __init__(self, pos, intensity=1,  color=(1, 1, 1), light_limit=15):
        self.pos = pos
        self.intensity = intensity
        self.color = color
        self.limit = light_limit


    def get_light_amount(self, dist):
        a = (self.color[0] * self.intensity, self.color[1] * self.intensity, self.color[2] * self.intensity)
        b = dist / self.limit
        return self.color[0] - a[0] * b, self.color[1] - a[1] * b, self.color[2] - a[2] * b
