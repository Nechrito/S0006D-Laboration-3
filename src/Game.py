from os import path

import pygame
import pygame.freetype

from src.Settings import *
from src.code.ai.Entity import Entity
from src.code.ai.behaviour.GlobalState import GlobalState
from src.code.ai.behaviour.states.IdleState import IdleState
from src.code.engine.Camera import CameraInstance
from src.code.engine.GameTime import GameTime
from src.code.engine.Renderer import Renderer
from src.code.environment.Map import Map
from src.code.environment.Tile import Tile
from src.code.math.Vector import vec2
from src.code.math.cMath import lerp


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

        pygame.display.set_caption(SETTINGS.TITLE)

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

        # mouse relative coords
        for agent in self.agents:
            CameraInstance.followTarget(self.relative)
            agent.update()
            agent.moveTo(self.relative)

        if not self.paused:

            pygame.display.set_caption(SETTINGS.TITLE +
                                       " | Speed: " +
                                       str(GameTime.timeScale) +
                                       " | FPS " +
                                       "{:.0f}".format(self.clock.get_fps()) +
                                       " | Date: " + GameTime.timeElapsed())

    def draw(self):
        self.renderer.clear()

        for tile in SETTINGS.TilesAll:
            self.renderer.renderTile(tile)

       # self.renderer.renderGrid()
       # self.renderer.renderRectOutline()

        if not self.realCursorEnabled:
            intersection = SETTINGS.getNode(self.relative)
            if intersection:
                x = intersection.position
                self.renderer.renderRect(SETTINGS.TILE_SCALE.tuple, x.tuple, (52, 52, 57), 200)

                for neighbour in intersection.neighbours:
                    node = SETTINGS.getNode(neighbour)
                    if node and node.isWalkable:
                        self.renderer.renderRect(SETTINGS.TILE_SCALE.tuple, neighbour.tuple, (0, 255, 128), 128)
                    else:
                        self.renderer.renderRect(SETTINGS.TILE_SCALE.tuple, neighbour.tuple, (255, 0, 128), 128)

                self.renderer.renderRect(SETTINGS.TILE_SCALE.tuple,
                                         self.relative.tuple,
                                         (37, 37, 38),
                                         200)

        for entity in self.agents:
            self.surface.blit(entity.image, CameraInstance.centeredSprite(entity))

            if len(entity.waypoints) > 0:
                self.renderer.renderRect([10, 10], entity.waypoints[-1].position)

            for i in range(0, len(entity.waypoints) - 1):
                self.renderer.renderLine(entity.waypoints[i].position, entity.waypoints[i + 1].position)

            (x, y) = (entity.position.X, entity.position.Y + SETTINGS.TILE_SCALE[1] - 5)
            self.renderer.renderRect((60, 18), (x - 30, y - 9), (0, 0, 0), 170)
            self.renderer.renderText(entity.name, (x, y), self.fontSmall)

        self.clock.tick(SETTINGS.MAX_FPS)

    def onClick(self):
        tile = self.selectedTile()
        if tile:
            tile.position.log()

    def selectedTile(self, position: vec2 = None):
        if not position:
            position = self.relative

        return SETTINGS.closestTile(position)

    def isObstacle(self, tile: Tile):
        for obstacle in SETTINGS.ObstacleTiles:
            if tile.rect.colliderect(obstacle.rect):
                return obstacle
        return None

    def setObstacle(self):
        tile = self.selectedTile()

        if not tile:
            return None

        obstacle = self.isObstacle(tile)

        if obstacle:
            SETTINGS.ObstacleTiles.remove(obstacle)
        else:
            SETTINGS.ObstacleTiles.append(tile)
