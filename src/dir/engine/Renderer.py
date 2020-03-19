import pygame
import pygame.freetype
from src.Settings import *
from src.dir.engine.CameraInstance import CameraInstance
from src.dir.math.Iterator import fori
from src.dir.math.Vector import vec2
from src.dir.pathfinding.Node import Node


class Renderer:

    def __init__(self, surface):
        self.surface = surface
        self.texts = []

    def clear(self):
        pygame.display.update()
        self.surface.fill((109, 247, 177))

    def renderTile(self, node: Node):
        for image in node.images:
            self.surface.blit(image, CameraInstance.centeredRect(node.rect))

    # doesn't follow camera like most else
    def renderRectToScreen(self, size, pos: vec2, color=(255, 255, 255), alpha=128):
        surface = pygame.Surface(size)
        surface.set_alpha(alpha)
        surface.fill(color)
        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        rect.center = pos.tuple
        self.surface.blit(surface, rect)

    def renderRect(self, size, pos, color=(255, 255, 255), alpha=128):
        surface = pygame.Surface(size)
        surface.set_alpha(alpha)
        surface.fill(color)
        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.surface.blit(surface, CameraInstance.centeredRect(rect))

    def renderRectOutline(self):
        for x in SETTINGS.Graph:
            for y in x:
                pygame.draw.rect(self.surface, (52, 52, 52), CameraInstance.centeredRect(y.rect))  # , 1

    def renderGrid(self):
        size = 16
        sWidth = SETTINGS.MAP_WIDTH
        sHeight = SETTINGS.MAP_HEIGHT
        color = (102, 227, 164)
        center = CameraInstance.center
        for x in fori(size, sWidth, size):
            pygame.draw.line(self.surface, color, (vec2(x, size) + center).tuple, (vec2(x, sHeight) + center).tuple)
        for y in fori(size, sHeight, size):
            pygame.draw.line(self.surface, color, (vec2(size, y) + center).tuple, (vec2(sWidth, y) + center).tuple)

    def renderLine(self, start: vec2, end: vec2, color=(255, 255, 255), width=1):
        v1 = vec2(start) + CameraInstance.center - vec2(8)
        v2 = vec2(end) + CameraInstance.center - vec2(8)
        pygame.draw.line(self.surface, color, v1.tuple, v2.tuple, width)

    def renderText(self, text: str, position, font, color=(255, 255, 255)):
        v1 = vec2(position) + CameraInstance.center
        fontRendered, fontRect = font.render(text, color)
        self.surface.blit(fontRendered, (v1.X - fontRect[2] / 2, v1.Y - fontRect[3] / 2))

    def renderTexts(self, position, font, color=(0, 0, 0)):
        for line in range(len(self.texts)):
            msg = self.texts[line]
            fontRendered, fontRect = font.render(msg, color)
            self.surface.blit(fontRendered, (position.X - fontRect[2] / 2, position.Y - fontRect[3] / 2))
            position.Y += font.size + 2

        self.texts.clear()

    def append(self, msg):
        self.texts.append(msg)
