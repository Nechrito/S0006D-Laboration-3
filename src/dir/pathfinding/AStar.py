import time
from copy import copy

from src.Settings import SETTINGS
from src.dir.math.Vector import vec2
from src.dir.pathfinding.IPath import IPath


class AStar(IPath):

    def __init__(self):
        super().__init__()

    def getPath(self, start: vec2, end: vec2):
        self.timerStart = time.time()
        self.timeElapsed = None

        if not start or not end:
            return

        startNode = SETTINGS.getNode(start, False, True)
        if not startNode:
            return

        endNode = SETTINGS.getNode(end, False, True)
        if not endNode:
            return

        closedList = []
        openList = [startNode]

        currentNode = None

        # iterate until end is located
        while 0 < len(openList) < 200 and len(closedList) < 200:

            currentNode = openList[0]
            currentIndex = 0

            for index, node in enumerate(openList):
                if node.f < currentNode.f:
                    currentNode = node
                    currentIndex = index

            openList.pop(currentIndex)
            closedList.append(currentNode)

            # complete, now reverse fill path
            if currentNode == endNode:
                break

            for temp in currentNode.neighbours:
                neighbour = copy(temp)

                if not neighbour or not neighbour.isWalkable:
                    continue

                if neighbour in closedList:
                    continue

                neighbour.parent = currentNode

                cost = currentNode.g + self.getCost(neighbour, currentNode)

                if neighbour in openList:
                    if neighbour.g > cost:
                        neighbour.g = cost
                else:
                    neighbour.g = cost
                    openList.append(neighbour)

                neighbour.h = self.heuristic(neighbour.position, endNode.position)
                neighbour.f = neighbour.g + neighbour.h

        path = self.backTrace(currentNode)

        #self.timeElapsed = truncate((time.time() - self.timerStart) * 1000)
        #avg = truncate(self.getAverage(PathType.AStar.value))
        #self.computeAverage(self.timeElapsed, PathType.AStar.value)
        #if self.timeElapsed > 0:
        #    print("[A*] Elapsed: " + str(self.timeElapsed) + "ms (Avg. " + str(avg) + "ms) | Path Length: " + str(len(path)))

        # if computation is completed, traverse list (todo: heap)
        return path
