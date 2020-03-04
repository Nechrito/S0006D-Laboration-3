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

        mapWidth = self.tmx.width * self.tmx.tilewidth
        mapHeight = self.tmx.height * self.tmx.tileheight
        SETTINGS.configure(mapWidth, mapHeight)

        self.start = vec2(0, 0)
        self.end = vec2(0, 0)
        self.loadPath()

        if reference:
            self.loadReferenceMap(reference)

    def loadPath(self):
        startTime = time.time()

        pathLayer = self.tmx.get_layer_by_name("Path")
        backgroundLayer = self.tmx.get_layer_by_name("Background")
        ti = self.tmx.get_tile_image_by_gid

        SETTINGS.TilesAll = []
        SETTINGS.PathTiles = []
        SETTINGS.ObstacleTiles = []
        SETTINGS.BackgroundTiles = []

        # loading progress
        inner = 0
        outer = 1
        innerSize = 0
        outerSize = 32702

        # This creates an 2D array, very quickly, through copying the same immutable object over and over again
        rows, cols = (SETTINGS.MAP_WIDTH, SETTINGS.MAP_HEIGHT)
        SETTINGS.Graph = [i[:] for i in [[0] * rows] * cols]

        innerSize = 96
        inner = 0
        outer += innerSize
        for x, y, gid in backgroundLayer:
            inner += 1
            #self.printLoadingProgress(inner, outer, innerSize, outerSize)

            tile = ti(gid)
            if tile:
                tileObj = Tile(vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1]), gid)
                tileObj.addImage(tile)
                SETTINGS.BackgroundTiles.append(tileObj)

        #print("[1] INNER: " + str(inner))
        innerSize = 9800
        inner = 0
        outer += innerSize
        for x, y, gid in pathLayer:
            inner += 1
            #self.printLoadingProgress(inner, outer, innerSize, outerSize)

            tile = ti(gid)
            if tile:
                position = vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1])

                tileObj = Tile(position, gid)
                tileObj.addImage(tile)
                SETTINGS.PathTiles.append(tileObj)

                SETTINGS.Graph[y][x] = Node(position)

        #print("[2] INNER: " + str(inner))
        innerSize = 3
        inner = 0
        outer += innerSize
        for layer in self.tmx.visible_layers:
            inner += 1
            #self.printLoadingProgress(inner, outer, innerSize, outerSize)

            for x, y, gid in layer:
                tile = ti(gid)
                if tile:
                    tileObj = Tile(vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1]), gid)
                    tileObj.addImage(tile)
                    SETTINGS.TilesAll.append(tileObj)


        # filter out nodes which are not filled in the path
        temp = []
        #print("[3] INNER: " + str(inner))

        innerSize = 1600
        inner = 0
        outer += innerSize
        for x in SETTINGS.Graph:
            inner += 1
            #self.printLoadingProgress(inner, outer, innerSize, outerSize)
            row = []
            for y in x:
                if str(y) != str(0):
                    y.addNeighbours()
                    row.append(y)
            if len(row) > 0:
                temp.append(row)

        SETTINGS.Graph = temp
        #print("[4] INNER: " + str(inner))

        #innerSize = 96
        #inner = 0
        #outer += innerSize
        #for col in range(len(SETTINGS.Graph)):
        #    inner = 0
        #    outer += innerSize
        #    self.printLoadingProgress(inner, outer, innerSize, outerSize)
        #    for row in range(len(SETTINGS.Graph[col])):
        #        inner += 1
        #        SETTINGS.Graph[col][row].addNeighbours()

        #print("[5] INNER: " + str(inner))
        for x in SETTINGS.Graph:
            print(x)

        timeElapsed = time.time() - startTime
        print("Loaded map in: " + str(truncate(timeElapsed * 1000)) + "ms")

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

                    # NOTE: B M T G V
                    if char == 'T':  # TREE TRÄD
                        tileObj.addImage(SETTINGS.TILE_T)
                        SETTINGS.TILES_T.append(tileObj)
                        SETTINGS.TilesAll.append(tileObj)
                    if char == 'M':  # GRASS? MARK?
                        tileObj.addImage(SETTINGS.TILE_M)
                        SETTINGS.TILES_M.append(tileObj)
                        SETTINGS.TilesAll.append(tileObj)
                    if char == 'B':  # WALL? RIVER?
                        tileObj.addImage(SETTINGS.TILE_B)
                        SETTINGS.TILES_B.append(tileObj)
                        SETTINGS.TilesAll.append(tileObj)
                    if char == 'G':  # COAL? GRÅTTA?
                        tileObj.addImage(SETTINGS.TILE_G)
                        SETTINGS.TILES_G.append(tileObj)
                        SETTINGS.TilesAll.append(tileObj)
                    if char == 'V':  # IRON? VATTEN?
                        tileObj.addImage(SETTINGS.TILE_V)
                        SETTINGS.TILES_V.append(tileObj)
                        SETTINGS.TilesAll.append(tileObj)
                    x += 1
                y += 1

    # DEPRECATED, JUST A REFERENCE
    def loadReferenceMapOld(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()[1:-1]
            y = 1
            for line in lines:
                x = 1
                line = line[1:-2]
                for char in line:
                    if char == 'X':
                        SETTINGS.ObstacleTiles.append(Tile(vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1])))
                    if char == 'S':
                        self.start = vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1])
                    if char == 'G':
                        self.end = vec2(x * SETTINGS.TILE_SCALE[0], y * SETTINGS.TILE_SCALE[1])

                    x += 1
                y += 1

        for col in range(len(SETTINGS.Graph)):
            for row in range(len(SETTINGS.Graph[col])):
                node = SETTINGS.Graph[col][row]
                node.addNeighbours()
                node.validate()

        #for col in SETTINGS.Graph:
            #print(str(col))