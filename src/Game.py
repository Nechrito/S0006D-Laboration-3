from os import path

import pygame
import pygame.freetype

from dir.engine.Camp import Camp
from dir.environment.Tree import Tree
from enums.EntityType import EntityType
from src.Settings import *
from src.dir.ai.Entity import Entity
from dir.ai.behaviour.GlobalState import GlobalState
from dir.ai.behaviour.IdleState import IdleState
from src.dir.engine.CameraInstance import CameraInstance
from src.dir.engine.GameTime import GameTime
from src.dir.engine.Renderer import Renderer
from src.dir.environment.Map import Map
from src.dir.math.Vector import vec2
from src.dir.math.cMath import lerp


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

        # Yes this is some next level fuckery, I'm on a deadline lol
        SETTINGS.TILE_B = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_B))
        SETTINGS.TILE_M = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_M))
        SETTINGS.TILE_T = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_T))
        SETTINGS.TILE_G = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_G))
        SETTINGS.TILE_V = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_V))

        self.map = Map(self.getRealFilePath(SETTINGS.MAP_PATH), self.getRealFilePath(SETTINGS.MAP_REF))

        self.fontSmall = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_BOLD), SETTINGS.SCREEN_HEIGHT * 16 // SETTINGS.SCREEN_WIDTH)
        self.fontRegular = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_REGULAR), SETTINGS.SCREEN_HEIGHT * 18 // SETTINGS.SCREEN_WIDTH)
        self.fontBold = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_BOLD), SETTINGS.SCREEN_HEIGHT * 22 // SETTINGS.SCREEN_WIDTH)

        campImg = pygame.image.load(self.getRealFilePath(SETTINGS.BUILDING_IMG))
        Camp.init(vec2(1024, 224), campImg)

        for treeTile in SETTINGS.TILES_T:
            tree = Tree(treeTile.position)
            Camp.treesContainer.append(tree)

        hatguyImg = pygame.image.load(self.getRealFilePath(SETTINGS.HATGUY_IMG))
        senseiImg = pygame.image.load(self.getRealFilePath(SETTINGS.SENSEI_IMG))

        self.entities = [ Entity(EntityType.Worker, Camp.position, hatguyImg, IdleState(), GlobalState()),
                          Entity(EntityType.Worker, Camp.position, hatguyImg, IdleState(), GlobalState()),
                          Entity(EntityType.Worker, Camp.position, hatguyImg, IdleState(), GlobalState()),
                          Entity(EntityType.Explorer, Camp.position, senseiImg, IdleState(), GlobalState()),
                          Entity(EntityType.Explorer, Camp.position, senseiImg, IdleState(), GlobalState()) ]

        self.realCursorEnabled = False
        pygame.mouse.set_visible(self.realCursorEnabled)
        pygame.event.set_grab(not self.realCursorEnabled)

        self.relative = Camp.position
        self.cursor = self.relative
        self.cursorSize = 9

        CameraInstance.init()
        CameraInstance.followTarget(Camp.position)

    def update(self):

        if not self.realCursorEnabled:
            CameraInstance.followTarget(self.relative)

            temp = pygame.mouse.get_pos()
            self.cursor = vec2(temp[0], temp[1])

            size = vec2(SETTINGS.MAP_WIDTH, SETTINGS.MAP_HEIGHT) + SETTINGS.SCREEN_RESOLUTION
            raw = self.cursor
            deltaX = min(1.0, max(1e-6, raw.X / size.X))
            deltaY = min(1.0, max(1e-6, raw.Y / size.Y))

            raw.X = lerp(raw.X, size.X, deltaX)
            raw.Y = lerp(raw.Y, size.Y, deltaY)

            self.relative = raw
        else:
            CameraInstance.followTarget(Camp.position)

        # fog of war
        self.checkFOW()

        if Camp.woodCount >= 2 and Camp.level == 1 or \
           Camp.woodCount >= 6 and Camp.level == 2 or \
           Camp.woodCount >= 12 and Camp.level == 3:
            Camp.levelUp(self.entities)

        # mouse relative coords
        for agent in self.entities:
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

        for row in SETTINGS.Graph:
            for node in row:
                if node and node.isVisible:
                    if CameraInstance.inCameraBounds(node.position):
                        self.renderer.renderTile(node)

       # self.renderer.renderGrid()
       # self.renderer.renderRectOutline()

        self.surface.blit(Camp.image, CameraInstance.centeredRect(Camp.rect))

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

        for entity in self.entities:
            # draw entity
            self.surface.blit(entity.image, CameraInstance.centeredSprite(entity))

            # draw waypoints
            for row in range(0, len(entity.waypoints) - 1):
                self.renderer.renderLine(entity.waypoints[row].position, entity.waypoints[row + 1].position)

            # draw entity type
            self.renderer.renderText(entity.name, entity.position + vec2(0, 16), self.fontSmall)

        # draw camp level
        #self.renderer.renderText("Camp (Lv. " + str(Camp.level) + ")", Camp.position - vec2(0, 32), self.fontBold)

        # draw information
        self.renderer.append("Camp Level: " + str(int(Camp.level)))
        self.renderer.append("Items to be collected: " + str(len(Camp.itemsContainer)))
        self.renderer.append("Wood: " + str(Camp.woodCount))
        self.renderer.append("Charcoal: " + str(Camp.charcoalCount))
        self.renderer.append("IronOres: " + str(Camp.ironOreCount))
        self.renderer.append("IronIngots: " + str(Camp.ironIngotCount))
        self.renderer.append("")
        self.renderer.append("Entities: " + str(len(self.entities)))


        centered = vec2(SETTINGS.SCREEN_WIDTH * 0.10, SETTINGS.SCREEN_HEIGHT * 0.10)
        self.renderer.renderTexts(centered, self.fontBold, (255, 255, 255))

        self.clock.tick(SETTINGS.MAX_FPS)

    def onClick(self):
        node = self.selectedNode()
        if node:
            node.position.log()
            if not node.isWalkable:
                return
            for agent in self.entities:
                if agent.entityType == EntityType.Explorer:
                    agent.moveTo(node.position.randomized())

    def checkFOW(self):
        # Computes the FOG OF WAR
        for agent in self.entities:
            node = SETTINGS.getNode(agent.position, False, False)

            i = 0
            searchRadius = 4 # the amount of neighbouring tiles to check
            if agent.entityType == EntityType.Explorer:
                searchRadius = 9

            while node and i <= searchRadius:

                #if not node.isVisible:
                    #SETTINGS.activateNode(node)

                for neighbour in node.neighbours:
                    if neighbour and neighbour.parent:
                        neighbourNode = SETTINGS.getNode(neighbour, False, False)
                        if neighbourNode and not neighbourNode.isVisible:
                            SETTINGS.activateNode(neighbourNode)
                            node = neighbourNode
                    else:
                        node = node.parent

                i += 1


    def selectedNode(self):
        return SETTINGS.closestNode(self.relative)
