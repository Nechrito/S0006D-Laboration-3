import pygame
import pygame.freetype
from src.Settings import *
from src.debug.engine.CameraInstance import CameraInstance
from src.debug.math.Iterator import fori
from src.debug.math.Vector import vec2
from src.debug.pathfinding.Node import Node


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
        #if not node.isVisible:
            #self.renderRect(SETTINGS.TILE_SIZE.tuple, node.position, (52, 52, 52), 230)

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
        tWidth = SETTINGS.TILE_SIZE[0]
        tHeight = SETTINGS.TILE_SIZE[1]
        sWidth = (SETTINGS.MAP_WIDTH - tWidth)
        sHeight = (SETTINGS.MAP_HEIGHT - tHeight)

        for x in fori(tWidth, sWidth, tWidth):
            self.renderLine(vec2(x, tHeight), vec2(x, sHeight))
        for y in fori(tHeight, sHeight, tHeight):
            self.renderLine(vec2(tWidth, y), vec2(sWidth, y))

    def renderLine(self, start: vec2, end: vec2, color=(255, 255, 255), width=1):
        v1 = vec2(start) + CameraInstance.center - vec2(8)
        v2 = vec2(end) + CameraInstance.center - vec2(8)
        pygame.draw.line(self.surface, color, v1.tuple, v2.tuple, width)

    def renderText(self, text: str, position, font, color=(255, 255, 255)):
        v1 = vec2(position) + CameraInstance.center
        fontRendered, fontRect = font.render(text, color)
        self.surface.blit(fontRendered, (v1.X - fontRect[2] / 2, v1.Y - fontRect[3] / 2))

    def renderTexts(self, position, font, color=(0, 0, 0)):
        if len(self.texts) <= 0:
            raise Exception("Use method .append(...) first to render multiple lines of text!")

        pos = (position[0], position[1])
        for line in range(len(self.texts)):
            msg = self.texts[line]
            self.renderText(msg, pos, font, color)
            pos = (pos[0], pos[1] + font.size + 2)

        self.texts.clear()

    def append(self, msg):
        self.texts.append(msg)
