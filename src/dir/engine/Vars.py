from typing import List

from dir.items.IPickupItem import IPickupItem
from dir.items.IronIngot import IronIngot
from dir.items.IronOre import IronOre
from dir.items.Tree import Tree
from dir.math.Vector import vec2


class Vars:

    campPosition: vec2 = None
    campRadius = 200

    treeCount      = 0
    charcoalCount  = 0
    ironIngotCount = 0
    ironOreCount   = 0
    swordCount     = 0
    soldierCount   = 0

    # contains all items which may be picked up
    itemsContainer:  List[IPickupItem] = []
    treesContainer:  List[Tree]        = []
    ingotsContainer: List[IronIngot]   = []
    oresContainer:   List[IronOre]     = []

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


