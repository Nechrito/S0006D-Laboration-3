from src.code.math.Vector import vec2
from src.code.pathfinding.AStar import AStar
from src.code.pathfinding.BreadthFirst import BreadthFirst
from src.code.pathfinding.DepthFirst import DepthFirst
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
        if waypoints and len(waypoints) >= 2:
            found = False
            for p in waypoints:
                if p.position.Local == end.Local:
                    found = True
                    break
            if found:
                return waypoints

        newPath = self.requestPath(start, end)
        return newPath

    def requestPath(self, start: vec2, end: vec2):
        self.algorithm.childNodes = []
        path = self.algorithm.getPath(start, end)

        if not path or len(path) <= 2:
            return None

        #if end.Local != path[-1].position.Local and end.Local != path[-2].position.Local:
           #return None

        found = False
        for p in path:
            if p.position == end:
                found = True
                break
        if not found:
            return None

        return path

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
