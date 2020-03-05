from os import path

import pygame
import pygame.freetype

from src.Settings import *
from src.code.ai.Entity import Entity
from src.code.ai.behaviour.Global import Global
from src.code.ai.behaviour.states.CollectState import Collect
from src.code.ai.behaviour.states.PurchasingState import Purchase
from src.code.ai.behaviour.states.SleepingState import Sleep
from src.code.engine.Camera import CameraInstance
from src.code.engine.GameTime import GameTime
from src.code.engine.Renderer import Renderer
from src.code.environment.AllBuildings import *
from src.code.environment.Map import Map
from src.code.environment.Tile import Tile
from src.code.math.Vector import vec2


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

        temp = pygame.mouse.get_pos()
        self.cursor = vec2(temp[0], temp[1])
        self.cursorSize = 9

        self.relative = vec2()

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

        self.font = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_REGULAR), SETTINGS.SCREEN_HEIGHT * 18 // SETTINGS.SCREEN_WIDTH)
        self.fontBold = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_BOLD), SETTINGS.SCREEN_HEIGHT * 22 // SETTINGS.SCREEN_WIDTH)

        self.entityImg = pygame.image.load(self.getRealFilePath(SETTINGS.ENTITY_SENSEI))
        self.buildings = ( getClub(), getDrink(), getResturant(),
                           getStore(), getStackHQ(), getHotel(),
                           getHangout(), getLTU() )

        sensei = pygame.image.load(self.getRealFilePath(SETTINGS.ENTITY_SENSEI))
        self.characterAlex = Entity("Alex", Sleep(), Global(), self.buildings[0].position, sensei)  #
        #self.characterWendy = Entity("Wendy", Collect(), Global(), self.buildings[1].position, sensei)
        #self.characterJohn = Entity("John", Purchase(), Global(), self.buildings[2].position, sensei)
        #self.characterJames = Entity("James", Collect(), Global(), self.buildings[3].position, sensei)

        self.agents = [self.characterAlex]

        CameraInstance.init()

    def update(self):

        CameraInstance.followTarget(self.relative)

        # mouse relative coords
        self.relative = vec2(self.cursor.X - CameraInstance.center.X, self.cursor.Y - CameraInstance.center.Y)
        for agent in self.agents:
            agent.update()
            #agent.moveTo(self.relative)

        if not self.paused:

            pygame.display.set_caption(SETTINGS.TITLE +
                                       " | Speed: " +
                                       str(GameTime.timeScale) +
                                       " | FPS " +
                                       "{:.0f}".format(self.clock.get_fps()) +
                                       " | Date: " + GameTime.timeElapsed())

        if not self.realCursorEnabled:
            temp = pygame.mouse.get_pos()
            self.cursor = vec2(temp[0], temp[1])

    def draw(self):

        self.renderer.clear()

        for tile in SETTINGS.TilesAll:
            self.renderer.renderTile(tile)

        self.drawEntitiesInfo()

        #for col in range(len(SETTINGS.Graph)):
            #for row in range(len(SETTINGS.Graph[col])):
                #node = SETTINGS.Graph[col][row]
                #self.renderer.renderText(str(col) + ":" + str(row), node.position + vec2(10, 10), self.font)

       #a self.renderer.renderGrid()

        if not self.realCursorEnabled:
            intersection = SETTINGS.closestNode(self.relative)
            if intersection:
                x = intersection.position
                self.renderer.renderRect(SETTINGS.TILE_SCALE, x.tuple, (52,52,57), 200)
                for neighbour in intersection.neighbours:
                    self.renderer.renderRect(SETTINGS.TILE_SCALE, neighbour.tuple, (0, 128, 128), 128)

            self.renderer.renderRect((8, 8), (self.relative.X - self.cursorSize+8, self.relative.Y - self.cursorSize+8), (37, 37, 38), 200)

        for entity in self.agents:
            self.surface.blit(entity.image, CameraInstance.centeredSprite(entity))

            if len(entity.waypoints) > 0:
                self.renderer.renderRect([10, 10], entity.waypoints[-1].position)

            for i in range(0, len(entity.waypoints) - 1):
                self.renderer.renderLine(entity.waypoints[i].position, entity.waypoints[i + 1].position, (255, 255, 255), 5)

            (x, y) = (entity.position.X, entity.position.Y + SETTINGS.TILE_SCALE[1] - 5)
            self.renderer.renderRect((60, 18), (x - 30, y - 9), (0, 0, 0), 170)
            self.renderer.renderText(entity.name, (x, y), self.font)

        #for building in self.buildings:
        #    self.renderer.renderText(building.name,
        #                             (building.position.X, building.position.Y - SETTINGS.TILE_SCALE[1] * 5),
        #                             self.fontBold)

        self.clock.tick(SETTINGS.MAX_FPS)

    def drawEntitiesInfo(self):

        count = 0
        for entity in self.agents:

            self.renderer.renderRect((150, 150), (count * 150, 50), (0, 0, 0), 160)

            self.renderer.append(entity.name + " (" + str(entity.stateMachine.currentState) + ")")
            self.renderer.append("Fatigue: {0}%".format("{:.0f}".format(float(entity.fatigue))))
            self.renderer.append("Hunger: {0}%".format("{:.0f}".format(float(entity.hunger))))
            self.renderer.append("Thirst: {0}%".format("{:.0f}".format(float(entity.thirst))))
            self.renderer.append("Bank: {0}$".format("{:.0f}".format(float(entity.bank))))
            self.renderer.renderTexts((25 + SETTINGS.SCREEN_WIDTH * 0.05 + 150 * count, SETTINGS.SCREEN_HEIGHT * 0.10), self.font,
                                      (255, 255, 255))

            count += 1

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
