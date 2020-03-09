import math
import sys

import pytmx
import time
from src.Settings import *
from src.code.environment.Tile import Tile
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

        self.start = vec2(0, 0)
        self.end = vec2(0, 0)
        self.loadPath()

        if reference:
            self.loadReferenceMap(reference)

        timeElapsed = time.time() - startTime
        print("Loaded map in: " + str(truncate(timeElapsed * 1000)) + "ms")

    def loadPath(self):
        pathLayer = self.tmx.get_layer_by_name("Path")
        ti = self.tmx.get_tile_image_by_gid

        SETTINGS.TilesAll = []
        SETTINGS.PathTiles = []

        # This creates an 2D array, very quickly, through copying the same immutable object over and over again
        rows, cols = (SETTINGS.MAP_WIDTH, SETTINGS.MAP_HEIGHT)
        SETTINGS.Graph = [i[:] for i in [[0] * rows] * cols]

        for x, y, gid in pathLayer:
            tile = ti(gid)
            if tile:
                position = vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1])
                nodeObj = Node(position)
                nodeObj.addNeighbours()
                SETTINGS.Graph[y][x] = nodeObj

        for layer in self.tmx.visible_layers:
            for x, y, gid in layer:
                tile = ti(gid)
                if tile:
                    tileObj = Tile(vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1]), gid)
                    tileObj.addImage(tile)
                    SETTINGS.TilesAll.append(tileObj)

        temp = []
        for x in SETTINGS.Graph:
            row = []
            for y in x:
                if str(y) != str(0):
                    y.addNeighbours()
                    row.append(y)
            if len(row) > 0:
                temp.append(row)
        SETTINGS.Graph = temp

    def printLoadingProgress(self, inner, outer, innerSize, outerSize):
        print("Loading... " + str(int(outer/max(1, outerSize))) + "% " + str(outer) + '/' + str(outerSize) + " -> " + str(inner) + '/' + str(innerSize))
        sys.stdout.write("\033[K")

    def loadReferenceMap(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()[1:-1]
            y = 1
            for line in lines:
                x = 1
                line = line[1:-2]
                for char in line:
                    tileObj = Tile(vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1]))

                    if char != 'M' and char != 'G':
                        SETTINGS.ObstacleTiles.append(tileObj)
                        moveSpeed = 1.0
                        if char == 'G':
                            moveSpeed = 0.5

                        SETTINGS.setNode(tileObj.position, False, moveSpeed)
                       # print(str(SETTINGS.getNode(tileObj.position).isWalkable))

                    # NOTE: B M T G V
                    if char == 'T':  # TREE
                        tileObj.addImage(SETTINGS.TILE_T)
                        SETTINGS.TILES_T.append(tileObj)
                    if char == 'M':  # GROUND
                        tileObj.addImage(SETTINGS.TILE_M)
                        SETTINGS.TILES_M.append(tileObj)
                    if char == 'B':  # MOUNTAIN
                        tileObj.addImage(SETTINGS.TILE_B)
                        SETTINGS.TILES_B.append(tileObj)
                    if char == 'G':  # WETLAND
                        tileObj.addImage(SETTINGS.TILE_G)
                        SETTINGS.TILES_G.append(tileObj)
                    if char == 'V':  # WATER
                        tileObj.addImage(SETTINGS.TILE_V)
                        SETTINGS.TILES_V.append(tileObj)
                    x += 1
                y += 1

            for x in SETTINGS.Graph:
                print(x)

            SETTINGS.TilesAll.extend(SETTINGS.TILES_T)
            SETTINGS.TilesAll.extend(SETTINGS.TILES_M)
            SETTINGS.TilesAll.extend(SETTINGS.TILES_B)
            SETTINGS.TilesAll.extend(SETTINGS.TILES_G)
            SETTINGS.TilesAll.extend(SETTINGS.TILES_V)
