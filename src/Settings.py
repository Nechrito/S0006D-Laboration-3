from copy import copy


class SETTINGS:
    SCREEN_RESOLUTION = None
    TITLE = "S0006D Strategic AI - Philip Lindh"

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768

    MAP_WIDTH = None
    MAP_HEIGHT = None
    GRID_BOUNDS = None
    TILE_SCALE = None

    MAX_FPS = 200

    # Resource files direct path
    MAP_PATH = "map/Map5.tmx"
    MAP_REF = "map/Map5Ref.txt"
    TILES_B = []
    TILES_M = []
    TILES_T = []
    TILES_G = []
    TILES_V = []

    # GAME GRID
    Graph = {}
    TilesAll = []
    PathTiles = []
    ObstacleTiles = []

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

        # upscaled tilesize
        scalex = max(16, SETTINGS.SCREEN_WIDTH // (cls.MAP_WIDTH // 16))
        scaley = max(16, SETTINGS.SCREEN_HEIGHT // (cls.MAP_HEIGHT // 16))

        from src.code.math.Vector import vec2
        cls.TILE_SCALE = vec2(scalex, scaley)

        cls.SCREEN_RESOLUTION = vec2(cls.SCREEN_WIDTH, cls.SCREEN_HEIGHT)

        cls.GRID_BOUNDS = (cls.SCREEN_WIDTH + scalex / 2, cls.SCREEN_HEIGHT + scaley / 2)

    @classmethod
    def getNode(cls, position, doCopy=True):
        try:
            if doCopy:
                return copy(cls.Graph[int(position.LocalY-1)][int(position.LocalX-1)])
            else:
                return cls.Graph[int(position.LocalY - 1)][int(position.LocalX - 1)]
        except IndexError:
            pass

        return cls.closestNode(position, False)

    @classmethod
    def setNode(cls, position, enabled, moveSpeed=-1.0):
        node = cls.getNode(position, False)
        if node:
            if moveSpeed != -1.0:
                node.moveSpeed = moveSpeed

            node.isWalkable = enabled

    @classmethod
    def closestNode(cls, position, allowInstant=True, allowIterate=True):
        if allowInstant:
            instant = cls.getNode(position)
            if instant:
                return instant

        # TODO: https://stackoverflow.com/questions/53257607/get-closest-coordinate-in-2d-array
        if allowIterate:
            closest = None
            distance = 0
            for i in cls.Graph:
                for j in i:
                    currentDist = j.position.distance(position)
                    if currentDist < distance or distance == 0:
                        distance = currentDist
                        closest = j
            return closest

    @classmethod
    def closestTile(cls, position = None):
        node = cls.getNode(position)
        if node:
            return node

        closest = None
        distance = 0
        for tile in cls.PathTiles:
            currentDist = tile.position.distance(position)
            if currentDist < distance or distance == 0:
                distance = currentDist
                closest = tile

        return closest

