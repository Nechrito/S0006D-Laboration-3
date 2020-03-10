import math
from copy import copy

from src.code.math.DynamicGraph import DynamicGraph


class SETTINGS:

    # WINDOW
    SCREEN_RESOLUTION = None
    TITLE = "S0006D Strategic AI - Philip Lindh"

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768

    MAP_WIDTH = None
    MAP_HEIGHT = None
    BOUNDARIES = None
    TILE_SIZE = None

    MAX_FPS = 200

    # RESOURCE PATHS
    MAP_PATH = "map/Map5.tmx"
    MAP_REF = "map/Map5Ref.txt"

    # REFERENCE CONTAINERS
    TILES_B = []
    TILES_M = []
    TILES_T = []
    TILES_G = []
    TILES_V = []

    # GRID CONTAINERS
    Graph = None
    Coordinates = None

    # ADDITIONAL TILE RESOURCES
    TILE_B = "tiles/B.png"
    TILE_M = "tiles/M.png"
    TILE_T = "tiles/T.png"
    TILE_G = "tiles/G.png"
    TILE_V = "tiles/V.png"

    ENTITY_SENSEI = "img/sensei.png"

    ICON_PATH = "icon/Game.png"
    FONT_BLACK = "fonts/Roboto-Black.ttf"
    FONT_BOLD = "fonts/Roboto-Bold.ttf"
    FONT_REGULAR = "fonts/Roboto-Regular.ttf"

    @classmethod
    def configure(cls, mapWidth, mapHeight):
        cls.MAP_WIDTH = mapWidth
        cls.MAP_HEIGHT = mapHeight

        scalex = max(16, cls.SCREEN_WIDTH // (cls.MAP_WIDTH // 16))
        scaley = max(16, cls.SCREEN_HEIGHT // (cls.MAP_HEIGHT // 16))

        cls.BOUNDARIES = (cls.SCREEN_WIDTH + scalex / 2, cls.SCREEN_HEIGHT + scaley / 2)

        from src.code.math.Vector import vec2
        cls.TILE_SIZE = vec2(scalex, scaley)
        cls.SCREEN_RESOLUTION = vec2(cls.SCREEN_WIDTH, cls.SCREEN_HEIGHT)

    @classmethod
    def getNode(cls, position, doCopy=True, allowIterate=True):
        node = None
        try:
            if doCopy:
                node = copy(cls.Graph[int(position.LocalY - 1)][int(position.LocalX - 1)])
            else:
                node = cls.Graph[int(position.LocalY - 1)][int(position.LocalX - 1)]
        except IndexError:
            pass

        if node and type(node) != DynamicGraph:
            return node

        if allowIterate:
            return cls.closestNode(position, False)

    @classmethod
    def addNode(cls, node):
        cached = cls.getNode(node.position, False, False)
        if not cached or type(cached) is DynamicGraph:  # add to graph if not yet added
            cached = cls.Graph[int(node.position.LocalY - 1)][int(node.position.LocalX - 1)] = node

        if len(cached.neighbours) <= 0:
            cached.addNeighbours()

        if cached.position not in cls.Coordinates:
            cls.Coordinates.append(cached)
        return cached

    @classmethod
    def activateNode(cls, node):
        cached = cls.getNode(node.position, False, False)
        if cached:
            cached.isVisible = True

    @classmethod
    def configureNode(cls, position, enabled, moveSpeed=-1.0):
        node = cls.getNode(position, False)
        if node:
            if moveSpeed != -1.0:
                node.moveSpeed = moveSpeed

            node.isWalkable = enabled
        else:
            from src.code.pathfinding.Node import Node
            cls.addNode(Node(position))

    @classmethod
    def closestNode(cls, target, allowInstant=True, allowIterate=True):

        if allowInstant:
            instant = cls.getNode(target, True, False)
            if instant:
                return instant

        if allowIterate:
            if len(cls.Coordinates) > 0:
                close = min(cls.Coordinates, key=lambda p: p.position.distance(target))
                if close:
                    closeNode = cls.closestNode(close.position, True, False)
                    if closeNode:
                        return closeNode
        return None
