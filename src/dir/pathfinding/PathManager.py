from src.dir.math.Vector import vec2
from src.dir.pathfinding.AStar import AStar
from src.dir.pathfinding.BreadthFirst import BreadthFirst
from src.dir.pathfinding.DepthFirst import DepthFirst
from src.enums.PathType import PathType


def getFullPath(waypoints, startIndex: int = 0):
    distance = 0
    for i in range(startIndex, len(waypoints) - 1):
        startP = waypoints[i].position
        nextP = waypoints[i + 1].position
        distance += (nextP - startP).length
    return distance


class PathManager:

    def __init__(self, pathType: PathType = 0):
        self.updateTime = 0
        self.pathType = pathType

        if pathType == PathType.AStar:
            self.algorithm = AStar()
        elif pathType == PathType.DFS:
            self.algorithm = DepthFirst()
        elif pathType == PathType.BFS:
            self.algorithm = BreadthFirst()

    def requestPathCached(self, waypoints, start: vec2, end: vec2):
        if waypoints and len(waypoints) >= 1:
            if waypoints[-1].position == end:
                return waypoints

        newPath = self.requestPath(start, end)
        return newPath

    def requestPath(self, start: vec2, end: vec2):
        self.algorithm.childNodes = []
        return self.algorithm.getPath(start, end)

    def requestChildren(self):
        return self.algorithm.childNodes

    def getAlgorithm(self):
        return self.algorithm

    def getPathType(self):
        return self.pathType

    def cutPath(self, owner, waypoints):
        indices = []
        for node in waypoints:
            if node.position.distance(owner.position) > owner.radius:
                indices.append(node)

        return indices