import pygame

from src.Settings import SETTINGS
from src.dir.math.Vector import vec2


class Node:
    def __init__(self, position=None, parent=None, gid=-1):
        if not position:
            self.position = vec2()
        else:
            self.position = position

        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

        self.ID = gid
        self.images = []
        self.rect = pygame.Rect(self.position.X, self.position.Y, SETTINGS.TILE_SIZE[0], SETTINGS.TILE_SIZE[1])

        self.moveSpeed = 1.0
        self.color = (58, 58, 57)
        self.isWalkable = True
        self.isVisible = False
        self.neighbours = []

    def addNeighbours(self):

        self.neighbours.clear()

        adjacent = [vec2(1, 0), vec2(-1, 0), vec2(0, 1), vec2(0, -1),  # Vertical / Horizontal
                    vec2(1, 1), vec2(-1, 1), vec2(1, -1), vec2(-1, -1)]  # Diagonal

        for direction in adjacent:

            neighbour = self.position + vec2(direction.X * 16, direction.Y * 16)
            node = SETTINGS.getNode(neighbour, False, False)

            if node:
                # node.parent = self
                self.neighbours.append(node)

    #def __getitem__(self, item):
    #    if item == 0:
    #        return self.position.X
    #    if item == 1:
    #        return self.position.Y

    def addImage(self, img):
        self.images = [img] + self.images

    def __repr__(self):
        return str(self.isWalkable) + '(x' + str(self.position.LocalX) + ', y' + str(self.position.LocalY) + ')'

    def __hash__(self):
        return hash(self.g) + hash(self.h) + hash(self.f) + hash(self.position)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

