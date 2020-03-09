from os import path

import pygame
import pygame.freetype

from src.Settings import *
from src.code.ai.Entity import Entity
from src.code.ai.behaviour.GlobalState import GlobalState
from src.code.ai.behaviour.states.IdleState import IdleState
from src.code.engine.CameraInstance import CameraInstance
from src.code.engine.GameTime import GameTime
from src.code.engine.Renderer import Renderer
from src.code.environment.Map import Map
from src.code.math.Vector import vec2
from src.code.math.cMath import lerp
from src.code.pathfinding.Node import Node


class Game:

    def getRealFilePath(self, fileName):
        return path.join(self.directory, self.folder + fileName)

    def __init__(self, directory, folder):
        self.directory = directory
        self.folder = folder

        pygame.init()
        pygame.mixer.init()
        pygame.freetype.init()

        self.surface = pygame.display.set_mode((SETTINGS.SCREEN_WIDTH, SETTINGS.SCREEN_HEIGHT))
        self.renderer = Renderer(self.surface)

        logo = pygame.image.load(self.getRealFilePath(SETTINGS.ICON_PATH))
        pygame.display.set_icon(logo)

        pygame.display.set_caption(SETTINGS.TITLE + " - LOADING...")

        self.clock = pygame.time.Clock()
        self.paused = False

        self.realCursorEnabled = False
        pygame.mouse.set_visible(self.realCursorEnabled)
        pygame.event.set_grab(not self.realCursorEnabled)

        # Yes this is some next level fuckery, I'm on a deadline lol
        SETTINGS.TILE_B = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_B))
        SETTINGS.TILE_M = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_M))
        SETTINGS.TILE_T = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_T))
        SETTINGS.TILE_G = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_G))
        SETTINGS.TILE_V = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_V))

        self.map = Map(self.getRealFilePath(SETTINGS.MAP_PATH), self.getRealFilePath(SETTINGS.MAP_REF))

        self.fontSmall = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_BOLD), SETTINGS.SCREEN_HEIGHT * 12 // SETTINGS.SCREEN_WIDTH)
        self.fontRegular = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_REGULAR), SETTINGS.SCREEN_HEIGHT * 18 // SETTINGS.SCREEN_WIDTH)
        self.fontBold = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_BOLD), SETTINGS.SCREEN_HEIGHT * 22 // SETTINGS.SCREEN_WIDTH)

        self.entityImg = pygame.image.load(self.getRealFilePath(SETTINGS.ENTITY_SENSEI))

        sensei = pygame.image.load(self.getRealFilePath(SETTINGS.ENTITY_SENSEI))
        self.agents = [Entity("Alex", IdleState(), GlobalState(), sensei, vec2(800, 704)),
                       Entity("John", IdleState(), GlobalState(), sensei, vec2(1072, 608)),
                       Entity("Alex", IdleState(), GlobalState(), sensei, vec2(1040, 720))]

        self.relative = self.agents[0].position
        self.cursor = self.relative
        self.cursorSize = 9

        CameraInstance.init()

    def update(self):

        if not self.realCursorEnabled:
            temp = pygame.mouse.get_pos()
            self.cursor = vec2(temp[0], temp[1])

            # Todo: Scale with map size
            size = vec2(SETTINGS.MAP_WIDTH, SETTINGS.MAP_HEIGHT) + SETTINGS.SCREEN_RESOLUTION
            raw = self.cursor
            deltaX = min(1.0, max(1e-6, raw.X / size.X))
            deltaY = min(1.0, max(1e-6, raw.Y / size.Y))

            raw.X = lerp(raw.X, size.X, deltaX)
            raw.Y = lerp(raw.Y, size.Y, deltaY)

            self.relative = raw

        # fog of war
        self.checkFOW()

        # mouse relative coords
        for agent in self.agents:
            CameraInstance.followTarget(self.relative)
            agent.update()

        # window title
        if not self.paused:

            pygame.display.set_caption(SETTINGS.TITLE +
                                       " | Speed: " +
                                       str(GameTime.timeScale) +
                                       " | FPS " +
                                       "{:.0f}".format(self.clock.get_fps()) +
                                       " | Date: " + GameTime.timeElapsed())

    def draw(self):
        self.renderer.clear()

        #for node in SETTINGS.TilesAll:
            #if CameraInstance.inCameraBounds(node.position):
            #self.renderer.renderTile(node)

        for row in SETTINGS.Graph:
            for node in row:
                if node and len(node.images) > 0:
                    if CameraInstance.inCameraBounds(node.position):
                        self.renderer.renderTile(node)

       # self.renderer.renderGrid()
       # self.renderer.renderRectOutline()

        if not self.realCursorEnabled:
            intersection = SETTINGS.getNode(self.relative)
            if intersection:
                x = intersection.position
                self.renderer.renderRect(SETTINGS.TILE_SIZE.tuple, x.tuple, (52, 52, 57), 200)

                for neighbour in intersection.neighbours:
                    node = SETTINGS.getNode(neighbour)
                    if node and node.isWalkable:
                        self.renderer.renderRect(SETTINGS.TILE_SIZE.tuple, neighbour.tuple, (0, 255, 128), 128)
                    else:
                        self.renderer.renderRect(SETTINGS.TILE_SIZE.tuple, neighbour.tuple, (255, 0, 128), 128)

                self.renderer.renderRect(SETTINGS.TILE_SIZE.tuple,
                                         self.relative.tuple,
                                         (37, 37, 38),
                                         200)

        for entity in self.agents:
            self.surface.blit(entity.image, CameraInstance.centeredSprite(entity))

            if len(entity.waypoints) > 0:
                self.renderer.renderRect([10, 10], entity.waypoints[-1].position)

            for row in range(0, len(entity.waypoints) - 1):
                self.renderer.renderLine(entity.waypoints[row].position, entity.waypoints[row + 1].position)

            (x, y) = (entity.position.X, entity.position.Y + SETTINGS.TILE_SIZE[1] - 5)
            self.renderer.renderRect((60, 18), (x - 30, y - 9), (0, 0, 0), 170)
            self.renderer.renderText(entity.name, (x, y), self.fontSmall)

        self.clock.tick(SETTINGS.MAX_FPS)

    def onClick(self):
        tile = self.selectedNode()
        if tile:
            tile.position.log()

            for agent in self.agents:
                agent.moveTo(tile.position)

    def checkFOW(self):
        # Computes the FOG OF WAR
        for agent in self.agents:
            node = SETTINGS.getNode(agent.position, False, False)
            if node:
                for neighbour in node.neighbours:
                    neighbourNode = SETTINGS.getNode(neighbour, True, False)
                    if neighbourNode and not neighbourNode.isVisible:
                        SETTINGS.activateNode(neighbourNode)

                        for extNeighbour in neighbourNode.neighbours:
                            extNeighbourNode = SETTINGS.getNode(extNeighbour, True, False)
                            if extNeighbourNode and not extNeighbourNode.isVisible:
                                SETTINGS.activateNode(extNeighbourNode)

    def selectedNode(self):
        return SETTINGS.closestNode(self.relative)
