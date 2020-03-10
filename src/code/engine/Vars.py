from code.math.Vector import vec2


class Vars:

    treeCount      = 0
    charcoalCount  = 0
    ironIngotCount = 0
    ironOreCount   = 0
    swordCount     = 0
    soldierCount   = 0

    treesContainer     = []
    buildingsContainer = []
    ingotsContainer    = []
    oresContainer      = []

    @classmethod
    def init(cls, campPos: vec2):
        cls.campPosition = campPos

    @classmethod
    def canProduceCharcoal(cls):
        return cls.treeCount >= 2

    @classmethod
    def canProduceIronIngot(cls):
        return cls.ironOreCount >= 2 and cls.charcoalCount >= 3

    @classmethod
    def canProduceSword(cls):
        return cls.ironIngotCount >= 1 and cls.charcoalCount >= 2


