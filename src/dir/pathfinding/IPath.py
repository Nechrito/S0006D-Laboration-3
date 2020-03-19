import math
import abc

from src.dir.math.Vector import vec2
from src.dir.pathfinding.Node import Node
from src.enums.PathType import PathType


class IPath(object, metaclass=abc.ABCMeta):

    def __init__(self):
        self.childNodes = []
        self.timerStart = None
        self.timeElapsed = None
        self.average = {PathType.AStar.value: [0, 0], PathType.BFS.value: [0, 0], PathType.DFS.value: [0, 0]}
        self.sqrt2 = math.sqrt(2)

    def computeAverage(self, value, index):
        if value <= 0:
            return
        self.average[index][0] += value
        self.average[index][1] += 1

    def getAverage(self, index):
        return self.average[index][0] / max(1, self.average[index][1])

    @abc.abstractmethod
    def getPath(self, start: vec2, end: vec2):
        pass

    #  Diagonal Manhattan
    def heuristic(self, startPos, endPos):
        dx = abs(startPos.X - endPos.X)
        dy = abs(startPos.Y - endPos.Y)
        D = 1
        D2 = self.sqrt2
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    def getCost(self, startNode: Node, endNode: Node):
        if int(endNode.position.X - startNode.position.X) == 0 or int(endNode.position.Y - startNode.position.Y) == 0:
            cost = 1  # horizontal/vertical cost
        else:
            cost = self.sqrt2  # diagonal cost
        return startNode.g + cost

    @staticmethod
    def backTrace(node):
        path = [node]
        while node and node.parent:
            node = node.parent
            path.append(node)
        path.reverse()
        return path

    def backTraceBi(self, node1, node2):
        path1 = self.backTrace(node1)
        path2 = self.backTrace(node2)
        path2.reverse()
        return path1 + path2

