import random

import pytmx
import time

from dir.engine.TaskManager import TaskManager
from src.Settings import *
from src.dir.math.Vector import vec2
from src.dir.math.cMath import truncate
from src.dir.pathfinding.Node import Node


class Map:
    def __init__(self, filename, reference=None):
        self.tmx = pytmx.load_pygame(filename, pixelalpha=True)

        startTime = time.time()

        mapWidth = self.tmx.width * self.tmx.tilewidth
        mapHeight = self.tmx.height * self.tmx.tileheight
        #print(str(self.tmx.width))
        #print(str(self.tmx.height))
        SETTINGS.configure(mapWidth, mapHeight)

        self.start = vec2(0, 0)
        self.end = vec2(0, 0)

        self.loadPath()
        #ParallelTask.addTask(self.loadPath, (), 1)

        if reference:
            self.loadReferenceMap(reference)
            #ParallelTask.addTask(self.loadReferenceMap, reference, 5)

        for i in SETTINGS.Graph:
            for j in i:
                if j:
                    node = SETTINGS.getNode(j.position, False, False)
                    if node:
                        j.addNeighbours()
                        node.addNeighbours()

        col = 0
        for i in SETTINGS.Graph:
            print(str(col) + " " + str(i))
            col += 1

        timeElapsed = time.time() - startTime
        print("\nLoaded map in: " + str(truncate(timeElapsed * 1000)) + "ms \n")

    def loadPath(self):
        ti = self.tmx.get_tile_image_by_gid
        for layer in self.tmx.visible_layers:
            for x, y, gid in layer:
                tile = ti(gid)
                if tile:
                    nodeObj = SETTINGS.getNode(vec2(x * SETTINGS.TILE_SIZE[0], y * SETTINGS.TILE_SIZE[1]), False, False)
                    if nodeObj:
                        nodeObj.addImage(tile)

    def loadReferenceMap(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

            y = 0
            for line in lines:
                y += 1

                x = 0
                for char in line:
                    x += 1

                    position = vec2(x * SETTINGS.TILE_SIZE[0], y * SETTINGS.TILE_SIZE[1])
                    nodeObj = SETTINGS.addNode(Node(position))

                    if not nodeObj:
                        continue

                    # NOTE: B M T G V
                    if char == 'T':  # TREE
                        SETTINGS.TILES_T.append(nodeObj)
                    if char == 'M':  # GROUND
                        nodeObj.addImage(SETTINGS.TILE_M)
                        SETTINGS.TILES_M.append(nodeObj)
                    if char == 'B':  # MOUNTAIN
                        nodeObj.addImage(SETTINGS.TILE_B)
                        SETTINGS.TILES_B.append(nodeObj)
                    if char == 'G':  # WETLAND

                        nodeRaw = SETTINGS.getNode(nodeObj.position, False, False)
                        if nodeRaw:
                            nodeRaw.moveSpeed = 0.50

                        nodeObj.addImage(SETTINGS.TILE_G)
                        SETTINGS.TILES_G.append(nodeObj)
                    if char == 'V':  # WATER
                        nodeObj.addImage(SETTINGS.TILE_V)
                        SETTINGS.TILES_V.append(nodeObj)

                    if char != 'M' and char != 'G' and char != 'T':
                        nodeRaw = SETTINGS.getNode(nodeObj.position, False, False)
                        if nodeRaw:
                            nodeRaw.isWalkable = False
