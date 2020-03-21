import random
import time
from os import path

import pygame
import pygame.freetype

from dir.ai.Telegram import Telegram
from dir.engine.EntityManager import EntityManager
from dir.engine.Map import Map
from dir.environment.Camp import Camp
from dir.environment.Item import Item
from dir.environment.Tree import Tree
from enums.BuildingType import BuildingType
from enums.EntityType import EntityType
from enums.ItemType import ItemType
from enums.MessageType import MessageType
from src.Settings import *
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
        #SETTINGS.TILE_T1 = treeImgBlue # pygame.image.load(self.getRealFilePath(SETTINGS.TILE_T))
        #SETTINGS.TILE_T2 = treeImgRed # pygame.image.load(self.getRealFilePath(SETTINGS.TILE_T))
        SETTINGS.TILE_G = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_G))
        SETTINGS.TILE_V = pygame.image.load(self.getRealFilePath(SETTINGS.TILE_V))

        self.map = Map(self.getRealFilePath(SETTINGS.MAP_PATH), self.getRealFilePath(SETTINGS.MAP_REF))

        self.fontSmall = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_BLACK), SETTINGS.SCREEN_HEIGHT * 15 // SETTINGS.SCREEN_WIDTH)
        self.fontRegular = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_BOLD), SETTINGS.SCREEN_HEIGHT * 16 // SETTINGS.SCREEN_WIDTH)
        self.fontBold = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_BOLD), SETTINGS.SCREEN_HEIGHT * 18 // SETTINGS.SCREEN_WIDTH)
        self.fontBig = pygame.freetype.Font(self.getRealFilePath(SETTINGS.FONT_BOLD), SETTINGS.SCREEN_HEIGHT * 22 // SETTINGS.SCREEN_WIDTH)

        treeImgRed = pygame.image.load(self.getRealFilePath(SETTINGS.TREE_IMG2))
        treeImgBlue = pygame.image.load(self.getRealFilePath(SETTINGS.TREE_IMG1))

        self.buildingImg = pygame.image.load(self.getRealFilePath(SETTINGS.BUILDING_IMG))
        self.buildingRect = self.buildingImg.get_rect()

        hatguyImg = pygame.image.load(self.getRealFilePath(SETTINGS.HATGUY_IMG))
        senseiImg = pygame.image.load(self.getRealFilePath(SETTINGS.SENSEI_IMG))

        Camp.init(vec2(1136, 448), self.buildingImg)
        EntityManager.init(Camp.position, hatguyImg, senseiImg)

        # scatter iron ores around map
        centreP = vec2(SETTINGS.MAP_WIDTH // 2, SETTINGS.MAP_HEIGHT // 2)
        maxDist = 48
        maxIterations = 6
        for i in range(60):
            Camp.items.append(Item(centreP.randomized(maxIterations, maxDist), ItemType.Ore))

        for treeTile in SETTINGS.TILES_T:
            i = random.randint(1, 2)
            if i == 1:
                treeImg = treeImgBlue
            else:
                treeImg = treeImgRed

            tree = Tree(treeTile.position, treeImg)
            Camp.trees.append(tree)

        EntityManager.register(EntityType.Worker)
        #EntityManager.register(EntityType.Worker)
        #EntityManager.register(EntityType.Explorer)
        EntityManager.register(EntityType.Explorer)

        self.realCursorEnabled = False
        pygame.mouse.set_visible(self.realCursorEnabled)
        pygame.event.set_grab(not self.realCursorEnabled)

        self.relative = Camp.position
        self.cursor = self.relative
        self.cursorSize = 9

        CameraInstance.init()
        CameraInstance.followTarget(Camp.position)

        self.lastSoldierTick = 0

    def tryProduceSoldier(self):
        if Camp.swordCount >= 1 and (time.time() - self.lastSoldierTick >= 60 or self.lastSoldierTick == 0):
            EntityManager.register(EntityType.Soldier)
            Camp.swordCount -= 1
            self.lastSoldierTick = time.time()

    def checkFOW(self):

        # Computes the FOG OF WAR
        for agent in EntityManager.entities:
            if agent.isComputingPath:
                continue

            node = SETTINGS.getNode(agent.position, False, False)
            if not node:
                continue

            node.isVisible = True

            if agent.entityType != EntityType.Explorer:
                continue

            for neighbour in node.neighbours:
                if neighbour:
                    neighbour.isVisible = True

                    # 2nd layer lol
                    for neighbour2 in neighbour.neighbours:
                        if neighbour2:
                            neighbour2.isVisible = True

    def onClick(self):
        node = SETTINGS.getNode(self.relative, False, False)
        if node:

            node.position.log()

            if not node.isWalkable:
                return

            for entity in EntityManager.getAllOfType(EntityType.Explorer):
                entity.moveTo(node.position.randomized())

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

        self.checkFOW()
        self.tryProduceSoldier()
        EntityManager.update()

        # level up
        if Camp.canLevelUp():

            nextLevel = Camp.nextLevel

            if nextLevel == 2:
                #EntityManager.register(EntityType.Worker)
                EntityManager.register(EntityType.Miner)
                EntityManager.register(EntityType.Craftsman)
                EntityManager.sendMessage(Telegram(messageType=MessageType.CraftRequest, entityType=EntityType.Craftsman, message=BuildingType.Mine))
            elif nextLevel == 3:
                #EntityManager.register(EntityType.Worker)
                #EntityManager.register(EntityType.Worker)
                EntityManager.register(EntityType.Smith)
                EntityManager.sendMessage(Telegram(messageType=MessageType.CraftRequest, entityType=EntityType.Craftsman, message=BuildingType.Smith))
            elif nextLevel == 4:
                #EntityManager.register(EntityType.Worker)
                #EntityManager.register(EntityType.Worker)
                EntityManager.register(EntityType.Smelter)
                EntityManager.sendMessage(Telegram(messageType=MessageType.CraftRequest, entityType=EntityType.Craftsman, message=BuildingType.Smelt))
            elif nextLevel == 5:
                #EntityManager.register(EntityType.Worker)
                #EntityManager.register(EntityType.Worker)
                EntityManager.sendMessage(Telegram(messageType=MessageType.CraftRequest, entityType=EntityType.Craftsman, message=BuildingType.TrainingCamp))

            Camp.levelUp()

            # only IdleState listens to this specific message
            EntityManager.sendMessage(Telegram(messageType=MessageType.StateChange, entityType=EntityType.Ignored))

            EntityManager.sendMessage(Telegram(messageType=MessageType.LevelUp, entityType=EntityType.Ignored))

        # window title
        if not self.paused:
            pygame.display.set_caption(SETTINGS.TITLE + " | Speed: " + str(GameTime.timeScale) + " | FPS " + "{:.0f}".format(self.clock.get_fps()) + " | Date: " + GameTime.timeElapsed())

    def draw(self):

        self.renderer.clear()

        #for node in SETTINGS.DiscoveredTiles:
            #self.renderer.renderTile(node)

        # lowest layer, the tiles
        for row in SETTINGS.Graph:
            for node in row:
                if node and node.isVisible:
                    self.renderer.renderTile(node)

        #self.renderer.renderGrid()

        # draws the base image
        self.surface.blit(Camp.image, CameraInstance.centeredRect(Camp.rect))

        # outline of the radius which entities rely on
        if Camp.level < Camp.maxLevel:
            pygame.draw.circle(self.surface, (255, 255, 255), CameraInstance.centeredVec(Camp.position).toInt.tuple, int(Camp.radius), 1)

        for tree in Camp.trees:
            treeNode = SETTINGS.getNode(tree.position, False, False)
            if treeNode and treeNode.isVisible:
                self.surface.blit(tree.image, CameraInstance.centeredRect(tree.rect))

        # draw buildings crafted
        for building in Camp.buildings:
            self.buildingRect.center = building.position.tuple
            self.surface.blit(self.buildingImg, CameraInstance.centeredRect(self.buildingRect))
            self.renderer.renderText(building.name, building.position, self.fontBig, (181, 181, 181))

        # draws the relative cursor with it's indicating neighbours
        if not self.realCursorEnabled:
            intersection = SETTINGS.getNode(self.relative, False, False)
            if intersection:
                x = intersection.position
                self.renderer.renderRect(SETTINGS.TILE_SIZE.tuple, x.tuple, (52, 52, 57), 200)

                for neighbour in intersection.neighbours:
                    if neighbour and neighbour.isWalkable:
                        self.renderer.renderRect(SETTINGS.TILE_SIZE.tuple, neighbour.position.tuple, (0, 255, 128), 128)
                    else:
                        self.renderer.renderRect(SETTINGS.TILE_SIZE.tuple, neighbour.position.tuple, (255, 0, 128), 128)

        for entity in EntityManager.entities:
            # draw entity
            self.surface.blit(entity.image, CameraInstance.centeredSprite(entity))

            # draw waypoints
            for row in range(0, len(entity.waypoints) - 1):
                self.renderer.renderLine(entity.waypoints[row].position, entity.waypoints[row + 1].position)

            # draw entity name (type)
            self.renderer.renderText(entity.name, entity.position + vec2(0, 18), self.fontBold, (232, 232, 232))

        for item in Camp.items:
            self.renderer.renderText('[' + item.name + ']', item.position + vec2(0, 30), self.fontSmall, item.color)

        # draw information
        self.renderer.append("Camp Level: " + str(int(Camp.level)))
        self.renderer.append("Wood: " + str(Camp.woodCount) + '/' + str(Camp.totalWoodCount))
        self.renderer.append("IronOres: " + str(Camp.ironOreCount) + '/' + str(Camp.totalOreCount))
        self.renderer.append("IronIngots: " + str(Camp.ironIngotCount))
        self.renderer.append("Charcoal: " + str(Camp.charcoalCount))
        self.renderer.append("Swords: " + str(Camp.swordCount))
        self.renderer.append("")
        self.renderer.append("~Entities~")
        self.renderer.append("Workers: " + str(len(EntityManager.getAllOfType(EntityType.Worker))))
        self.renderer.append("Explorers: " + str(len(EntityManager.getAllOfType(EntityType.Explorer))))
        self.renderer.append("Craftsmen: " + str(len(EntityManager.getAllOfType(EntityType.Craftsman))))
        self.renderer.append("Miners: " + str(len(EntityManager.getAllOfType(EntityType.Miner))))
        self.renderer.append("Smelters: " + str(len(EntityManager.getAllOfType(EntityType.Smelter))))
        self.renderer.append("Smiths: " + str(len(EntityManager.getAllOfType(EntityType.Smith))))
        self.renderer.append("Soldiers: " + str(Camp.soldierCount))

        centered = vec2(SETTINGS.SCREEN_WIDTH * 0.10, SETTINGS.SCREEN_HEIGHT * 0.015)
        self.renderer.renderRectToScreen((150, 445), centered, (37, 37, 38), 200)
        self.renderer.renderTexts(centered, self.fontBold, (255, 255, 255))

        self.clock.tick(SETTINGS.MAX_FPS)
