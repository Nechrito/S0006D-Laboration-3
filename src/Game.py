import random
import threading
from os import path

import pygame
import pygame.freetype

from dir.ai.behaviour.GlobalState import GlobalState
from dir.ai.behaviour.IdleState import IdleState
from dir.ai.behaviour.artisan.CraftState import CraftState
from dir.ai.behaviour.artisan.MineState import MineState
from dir.ai.behaviour.artisan.SmeltState import SmeltState
from dir.ai.behaviour.artisan.SmithState import SmithState
from dir.engine.Map import Map
from dir.environment.Camp import Camp
from dir.environment.Item import Item
from dir.environment.Tree import Tree
from enums.EntityType import EntityType
from enums.ItemType import ItemType
from src.Settings import *
from src.dir.ai.Entity import Entity
from src.dir.engine.CameraInstance import CameraInstance
from src.dir.engine.GameTime import GameTime
from src.dir.engine.Renderer import Renderer
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

        treeImgBlue = pygame.image.load(self.getRealFilePath(SETTINGS.TREE_IMG1))
        treeImgRed = pygame.image.load(self.getRealFilePath(SETTINGS.TREE_IMG2))
        treeImgBlue = pygame.transform.scale(treeImgBlue, (32, 48))
        treeImgRed = pygame.transform.scale(treeImgRed, (32, 48))

        # Yes this is some next level fuckery, I'm on a deadline lol
        SETTINGS.TILE_B = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_B))
        SETTINGS.TILE_M = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_M))
        SETTINGS.TILE_T1 = treeImgBlue # pygame.image.load(self.getRealFilePath(SETTINGS.TILE_T))
        SETTINGS.TILE_T2 = treeImgRed # pygame.image.load(self.getRealFilePath(SETTINGS.TILE_T))
        SETTINGS.TILE_G = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_G))
        SETTINGS.TILE_V = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_V))

        self.map = Map(self.getRealFilePath(SETTINGS.MAP_PATH), self.getRealFilePath(SETTINGS.MAP_REF))

        self.fontSmall = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_BOLD), SETTINGS.SCREEN_HEIGHT * 16 // SETTINGS.SCREEN_WIDTH)
        self.fontRegular = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_REGULAR), SETTINGS.SCREEN_HEIGHT * 18 // SETTINGS.SCREEN_WIDTH)
        self.fontBold = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_BOLD), SETTINGS.SCREEN_HEIGHT * 22 // SETTINGS.SCREEN_WIDTH)

        campImg = pygame.image.load(self.getRealFilePath(SETTINGS.BUILDING_IMG))
        Camp.init(vec2(1152, 256), campImg)

        # scatter iron ores around map
        centreP = vec2(SETTINGS.MAP_WIDTH / 2, SETTINGS.MAP_HEIGHT / 2)
        maxDist = 48
        maxIterations = 4
        for i in range(60):
            Camp.itemsContainer.append(Item(centreP.randomized(maxIterations, maxDist), ItemType.IronOre))

        for treeTile in SETTINGS.TILES_T:
            tree = Tree(treeTile.position)
            Camp.treesContainer.append(tree)

        self.hatguyImg = pygame.image.load(self.getRealFilePath(SETTINGS.HATGUY_IMG))
        self.senseiImg = pygame.image.load(self.getRealFilePath(SETTINGS.SENSEI_IMG))

        self.entities = [ Entity(EntityType.Worker,   Camp.position, self.hatguyImg, IdleState(), GlobalState()),
                          Entity(EntityType.Explorer, Camp.position, self.senseiImg, IdleState(), GlobalState()) ]

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
        t = threading.Thread(target=self.checkFOW, args=())
        t.start()
        t.join()

        if Camp.woodCount / Camp.level == 4:
            for entity in self.entities:
                if entity.entityType == EntityType.Worker:
                    rand = random.randint(1, 4)
                    if rand == 1:
                        entity.setState(CraftState())
                    elif rand == 2:
                        entity.setState(MineState())
                    elif rand == 3:
                        entity.setState(SmeltState())
                    elif rand == 4:
                        entity.setState(SmithState())

            self.entities.append(Entity(EntityType.Explorer, Camp.position, self.senseiImg, IdleState(), GlobalState()))
            self.entities.append(Entity(EntityType.Worker, Camp.position, self.hatguyImg, IdleState(), GlobalState()))
            self.entities.append(Entity(EntityType.Worker, Camp.position, self.hatguyImg, IdleState(), GlobalState()))

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

        # lowest layer, the tiles
        for row in SETTINGS.Graph:
            for node in row:
                if node and node.isVisible:
                    if CameraInstance.inCameraBounds(node.position):
                        self.renderer.renderTile(node)

        # draw placeholders for buildings
        for building in Camp.buildings:
            self.renderer.renderRect((16, 16), building.position)
            self.renderer.renderText(building.name, building.position, self.fontRegular)

        for item in Camp.itemsContainer:
            self.renderer.renderRect((4, 4), item.position)
            self.renderer.renderText(item.name, item.position, self.fontSmall)

       # self.renderer.renderGrid()
       # self.renderer.renderRectOutline()

        # draws the base image
        self.surface.blit(Camp.image, CameraInstance.centeredRect(Camp.rect))

        # draws the relative cursor with it's indicating neighbours
        if not self.realCursorEnabled:
            intersection = SETTINGS.getNode(self.relative, False, False)
            if intersection:
                x = intersection.position
                self.renderer.renderRect(SETTINGS.TILE_SIZE.tuple, x.tuple, (52, 52, 57), 200)

                for neighbour in intersection.neighbours:
                    node = SETTINGS.getNode(neighbour)
                    if node and node.isWalkable:
                        self.renderer.renderRect(SETTINGS.TILE_SIZE.tuple, neighbour.tuple, (0, 255, 128), 128)
                    else:
                        self.renderer.renderRect(SETTINGS.TILE_SIZE.tuple, neighbour.tuple, (255, 0, 128), 128)

                self.renderer.renderRect(SETTINGS.TILE_SIZE.tuple, self.relative.tuple, (37, 37, 38), 200)

        for entity in self.entities:
            # draw entity
            self.surface.blit(entity.image, CameraInstance.centeredSprite(entity))

            # draw waypoints
            for row in range(0, len(entity.waypoints) - 1):
                self.renderer.renderLine(entity.waypoints[row].position, entity.waypoints[row + 1].position)

            # draw entity type
            self.renderer.renderText(entity.name, entity.position + vec2(0, 16), self.fontSmall)

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
        self.renderer.renderRect((150, 150), centered, (37, 37, 38), 200)
        self.renderer.renderTexts(centered, self.fontBold, (255, 255, 255))

        self.clock.tick(SETTINGS.MAX_FPS)

    def onClick(self):
        node = SETTINGS.getNode(self.relative, False, False)
        if node:
            node.position.log()
            if not node.isWalkable:
                return
            for entity in self.entities:
                if entity.entityType == EntityType.Explorer:
                    t = threading.Thread(target=entity.moveTo, args=(node.position.randomized(4, 4),))
                    t.start()
                    t.join()

    def checkFOW(self):
        # Computes the FOG OF WAR
        for agent in self.entities:
            if agent.entityType != EntityType.Explorer:
                searchRadius = 3
            else:
                searchRadius = 8  # the amount of neighbouring tiles to check

            node = SETTINGS.getNode(agent.position, False, False)

            i = 0
            while node and i <= searchRadius:
                i += 1
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
