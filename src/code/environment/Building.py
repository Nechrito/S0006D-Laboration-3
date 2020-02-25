import random

from src.code.math.Vector import vec2


class Building:
    def __init__(self, position, name: str, description: str = None):
        self.position = position
        self.name = name
        self.description = description

        threshold = 30
        self.randomized = vec2(self.position.X + random.randrange(-threshold, threshold), self.position.Y + random.randrange(-threshold, threshold / 2))