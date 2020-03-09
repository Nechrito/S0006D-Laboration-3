import math
import sys

import pytmx
import time
from src.Settings import *
from src.code.math.DynamicGraph import DynamicGraph
from src.code.math.Vector import vec2
from src.code.math.cMath import truncate
from src.code.pathfinding.Node import Node


class Map:
    def __init__(self, filename, reference=None):
        self.tmx = pytmx.load_pygame(filename, pixelalpha=True)

        startTime = time.time()

        mapWidth = self.tmx.width * self.tmx.tilewidth
        mapHeight = self.tmx.height * self.tmx.tileheight
        SETTINGS.configure(mapWidth, mapHeight)

        SETTINGS.Graph = DynamicGraph()
        SETTINGS.Coordinates = []

        self.start = vec2(0, 0)
        self.end = vec2(0, 0)

        if reference:
            self.loadReferenceMap(reference)

        self.loadPath()

        timeElapsed = time.time() - startTime
        print("Loaded map in: " + str(truncate(timeElapsed * 1000)) + "ms")

    def loadPath(self):
        ti = self.tmx.get_tile_image_by_gid
        backgroundLayer = self.tmx.get_layer_by_name("Background")
        pathLayer = self.tmx.get_layer_by_name("Path")

        for x, y, gid in backgroundLayer:
            tile = ti(gid)
            if tile:
                nodeObj = SETTINGS.getNode(vec2(x * SETTINGS.TILE_SIZE[0], y * SETTINGS.TILE_SIZE[1]), False, False)
                nodeObj.addImage(tile)
        for x, y, gid in pathLayer:
            tile = ti(gid)
            if tile:
                nodeObj = SETTINGS.getNode(vec2(x * SETTINGS.TILE_SIZE[0], y * SETTINGS.TILE_SIZE[1]), False, False)
                nodeObj.addImage(tile)

    def loadReferenceMap(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()[1:-1]
            y = 1
            for line in lines:
                x = 1
                line = line[1:-2]
                for char in line:
                    position = vec2(x * SETTINGS.TILE_SIZE[0], y * SETTINGS.TILE_SIZE[1])
                    nodeObj = SETTINGS.addNode(Node(position))

                    # NOTE: B M T G V
                    if char == 'T':  # TREE
                        nodeObj.addImage(SETTINGS.TILE_T)
                        SETTINGS.TILES_T.append(nodeObj)
                    if char == 'M':  # GROUND
                        nodeObj.addImage(SETTINGS.TILE_M)
                        SETTINGS.TILES_M.append(nodeObj)
                    if char == 'B':  # MOUNTAIN
                        nodeObj.addImage(SETTINGS.TILE_B)
                        SETTINGS.TILES_B.append(nodeObj)
                    if char == 'G':  # WETLAND
                        nodeObj.addImage(SETTINGS.TILE_G)
                        SETTINGS.TILES_G.append(nodeObj)
                    if char == 'V':  # WATER
                        nodeObj.addImage(SETTINGS.TILE_V)
                        SETTINGS.TILES_V.append(nodeObj)

                    if char != 'M' and char != 'G':
                        moveSpeed = 1.0
                        if char == 'G':
                            moveSpeed = 0.5

                        SETTINGS.configureNode(nodeObj.position, False, moveSpeed)

                    x += 1
                y += 1

            col = 0
            for x in SETTINGS.Graph:
                print(str(col) + " " + str(x))
                col += 1

            #SETTINGS.TilesAll.extend(SETTINGS.TILES_T)
            #SETTINGS.TilesAll.extend(SETTINGS.TILES_M)
            #SETTINGS.TilesAll.extend(SETTINGS.TILES_B)
            #SETTINGS.TilesAll.extend(SETTINGS.TILES_G)
            #SETTINGS.TilesAll.extend(SETTINGS.TILES_V)
