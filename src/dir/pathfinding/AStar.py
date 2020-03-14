import time

from dir.engine.GameTime import GameTime
from src.Settings import SETTINGS
from src.dir.math.Vector import vec2
from src.dir.math.cMath import truncate
from src.dir.pathfinding.IPath import IPath
from src.enums.PathType import PathType


class AStar(IPath):

    def __init__(self):
        super().__init__()

    def getPath(self, start: vec2, end: vec2):
        self.timerStart = time.time()
        self.timeElapsed = None

        startNode = SETTINGS.getNode(start, False, True)
        endNode = SETTINGS.getNode(end, False, True)

        closedList = []
        openList = [startNode]

        currentNode = None

        # iterate until end is located
        while openList:
            currentNode = openList[0]
            currentIndex = 0

            for index, node in enumerate(openList):
                if node.f < currentNode.f and node.isWalkable:
                    currentNode = node
                    currentIndex = index

            openList.pop(currentIndex)
            closedList.append(currentNode.position)

            if not currentNode.isWalkable:
                continue

            # complete, now reverse fill path
            if currentNode == endNode:
                break

            for pos in currentNode.neighbours:

                if pos in closedList:
                    continue

                neighbour = SETTINGS.getNode(pos)

                if not neighbour or not neighbour.isWalkable:
                    continue

                neighbour.parent = currentNode

                if neighbour not in self.childNodes:
                    self.childNodes.append(neighbour)

                cost = currentNode.g + self.getCost(neighbour, currentNode)

                if neighbour in openList:
                    if neighbour.g > cost:
                        neighbour.g = cost
                else:
                    neighbour.g = cost
                    openList.append(neighbour)

                neighbour.h = self.heuristic(neighbour.position, endNode.position)
                neighbour.f = neighbour.g + neighbour.h

        # if computation is completed, traverse list (todo: heap)
        path = self.backTrace(currentNode)

        self.timeElapsed = truncate((time.time() - self.timerStart) * 1000)
        avg = truncate(self.getAverage(PathType.AStar))

        self.computeAverage(self.timeElapsed, PathType.AStar)

        if self.timeElapsed > 0:
            print("[A*] Elapsed: " + str(self.timeElapsed) +
                  "ms (Avg. " + str(avg) +
                  "ms) | Path Length: " + str(len(path)))

        return path

