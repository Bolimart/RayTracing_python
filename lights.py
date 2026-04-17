from material import Material


class Light:

    def __init__(self, pos, material: Material, intensity=1, light_limit=15):
        self.material = material
        self.pos = pos
        self.intensity = intensity
        self.limit = light_limit
