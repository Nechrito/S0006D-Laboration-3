import pygame
from src.Settings import *
from src.dir.engine.GameTime import GameTime
from src.dir.math.Vector import vec2


class CameraInstance:
    center: vec2
    rect: pygame.Rect
    mapWidth: int
    mapHeight: int

    @classmethod
    def init(cls):
        cls.center = vec2()
        cls.rect = pygame.Rect(0, 0, SETTINGS.MAP_WIDTH, SETTINGS.MAP_HEIGHT)
        cls.mapWidth = cls.rect[2]
        cls.mapHeight = cls.rect[3]
        cls.bounds = SETTINGS.TILE_SIZE

    @classmethod
    def centeredRect(cls, rect):
        return rect.move(cls.rect.topleft)

    @classmethod
    def centeredSprite(cls, sprite):
        return sprite.rect.move(cls.rect.topleft)

    @classmethod
    def centeredVec(cls, position):
        return position + cls.center

    @classmethod
    def followTarget(cls, target):

        centerx = (-target.X + SETTINGS.SCREEN_WIDTH / 2) - cls.center.X
        centery = (-target.Y + SETTINGS.SCREEN_HEIGHT / 2) - cls.center.Y

        cls.center += vec2(centerx, centery) * GameTime.fixedDeltaTime * 2

        #  Make sure we're within map boundaries
        xMin = min(-SETTINGS.TILE_SIZE[0], cls.center.X)
        yMin = min(-SETTINGS.TILE_SIZE[0], cls.center.Y)

        xMax = max(-(cls.mapWidth - SETTINGS.SCREEN_WIDTH + SETTINGS.TILE_SIZE[0]), xMin)
        yMax = max(-(cls.mapHeight - SETTINGS.SCREEN_HEIGHT + SETTINGS.TILE_SIZE[0]), yMin)

        cls.center = vec2(xMax, yMax)
        cls.rect = pygame.Rect(cls.center.X, cls.center.Y, cls.mapWidth, cls.mapHeight)

    @classmethod
    def inCameraBounds(cls, position):
        boundsMin = SETTINGS.TILE_SIZE
        maxWidth = SETTINGS.SCREEN_WIDTH + boundsMin[0]
        maxHeight = SETTINGS.SCREEN_HEIGHT + boundsMin[1]
        delta = cls.center + position
        return -boundsMin[0] < delta.X < maxWidth and -boundsMin[1] < delta.Y < maxHeight