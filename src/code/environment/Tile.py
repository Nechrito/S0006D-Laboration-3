import pygame

from src.Settings import *
from src.code.math.Vector import vec2


class Tile:

    def __init__(self, position: vec2, gid = -1):
        self.ID = gid
        self.position = position
        self.image = None
        self.rect = pygame.Rect(position.X, position.Y, SETTINGS.TILE_SCALE[0], SETTINGS.TILE_SCALE[1])

    def __hash__(self):
        return hash(self.position)

    def __eq__(self, other):
        return (self.ID != -1 and self.ID == other.ID) or self.position == other.position

    def __repr__(self):
        return "Tile"

    def addImage(self, img):
        self.image = img
