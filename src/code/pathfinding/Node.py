import pygame

from src.Settings import SETTINGS
from src.code.math.Vector import vec2
from src.code.math.cMath import lerp, lerpColor


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

        if 0 < self.position.X < SETTINGS.MAP_WIDTH - SETTINGS.TILE_SIZE[0] and 0 < self.position.Y < SETTINGS.MAP_HEIGHT - SETTINGS.TILE_SIZE[1]:
            self.isWalkable = True

        self.neighbours.clear()

        adjacent = [vec2(1, 0), vec2(-1, 0), vec2(0, 1), vec2(0, -1),  # Vertical / Horizontal
                    vec2(1, 1), vec2(-1, 1), vec2(1, -1), vec2(-1, -1)]  # Diagonal

        for direction in adjacent:
            neighbour = self.position + vec2(direction.X * SETTINGS.TILE_SIZE[0], direction.Y * SETTINGS.TILE_SIZE[1])

            if 0 < neighbour.X < SETTINGS.MAP_WIDTH - SETTINGS.TILE_SIZE[0] and 0 < neighbour.Y < SETTINGS.MAP_HEIGHT - SETTINGS.TILE_SIZE[1]:
                self.neighbours.append(neighbour)

    def updateColors(self, distanceCovered, distanceTotal):
        delta = min(1.0, max(1e-4, distanceCovered / distanceTotal))
        colorMax = 255.0
        colorMin = 0.0
        colorByDist = ((lerp(colorMax * 0.00, colorMax * 1.00, delta)), 0, 0)
        mergeColor = (0, 20, 252)
        self.color = lerpColor(mergeColor, colorByDist, delta)
        return self.color

    def __getitem__(self, item):
        if item == 0:
            return self.position.X
        if item == 1:
            return self.position.Y

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

