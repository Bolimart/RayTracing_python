

class Light:

    def __init__(self, pos, intensity=1, color=(1, 1, 1), light_limit=15):
        self.pos = pos
        self.intensity = intensity
        self.color = (color[0] * intensity, color[1] * intensity, color[2] * intensity)
        self.base_color = color
        self.limit = light_limit


    def get_light_amount(self, dist):
        b = dist / self.limit
        return self.color[0] - self.color[0] * b, self.color[1] - self.color[1] * b, self.color[2] - self.color[2] * b
