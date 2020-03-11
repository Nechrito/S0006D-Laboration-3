import time

from src.Settings import SETTINGS
from src.debug.math.Vector import vec2
from src.debug.math.cMath import truncate
from src.debug.pathfinding.Node import Node
from src.debug.pathfinding.IPath import IPath
from src.enums.PathType import PathType


class BreadthFirst(IPath):
    def __init__(self):
        super().__init__()
        self.queue = []
        self.timerStart = time.time()
        self.timeElapsed = None

    def getPath(self, start: vec2, end: vec2):

        self.timerStart = time.time()
        self.timeElapsed = None

        startNode = SETTINGS.getNode(start, False, False)
        self.queue = []
        self.queue.append(startNode)

        pathDict = {startNode: False}
        currentNode = None

        while self.queue:

            currentNode = self.queue.pop(0)
            self.childNodes.append(currentNode)

            if currentNode is None or currentNode.position == end:
                break

            for childPos in currentNode.neighbours:
                neighbour = SETTINGS.getNode(childPos)
                if not neighbour:
                    continue

                neighbour.parent = currentNode

                if neighbour.isWalkable and neighbour not in pathDict:
                    self.queue.append(neighbour)
                    pathDict[neighbour] = currentNode.position - neighbour.position

        path = self.backTrace(currentNode)

        self.timeElapsed = (time.time() - self.timerStart) * 1000
        self.computeAverage(self.timeElapsed, PathType.BFS)
        print("[BFS] Elapsed: " + str(truncate(self.timeElapsed)) + "ms (Avg. " + str(truncate(self.getAverage(PathType.BFS))) + "ms) | Path Length: " + str(len(path)))

        return path
