# Since 3.7 this allows to remove annotations from type hinting when doing conditional import
from __future__ import annotations

# Conditional import (hinting, avoids circular imports)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dir.environment.Building import Building
    from dir.environment.Item import Item
    from dir.environment.Tree import Tree

# packages
import pygame
import time
from typing import List

# local packages
from dir.engine.GameTime import GameTime
from dir.math.Vector import vec2
from enums.BuildingType import BuildingType


class Camp:

    level = 1
    nextLevel = 2
    maxLevel = 6
    radius = 220
    position: vec2
    image: pygame.Surface
    imageScale: vec2
    rect: pygame.Rect

    # temporary hack, see IdleState.py
    lastLevelUpTick = 0

    # entity cap
    entitiesCount = 200

    # gathered/produced
    woodCount      = 0
    charcoalCount  = 0
    ironIngotCount = 0
    ironOreCount   = 0
    swordCount     = 0
    soldierCount   = 0

    # contains all items which may be picked up
    items: List[Item] = []

    # the trees scattered around the map
    trees: List[Tree] = []

    # complexes which may be used primarily by artisans
    buildings: List[Building] = []

    @classmethod
    def init(cls, campPos: vec2, image):
        cls.position = campPos

        cls.imageScale = vec2(70, 88) # could do image.get_width() / height() aswell but can't be arsed right now
        cls.image = pygame.transform.scale(image, cls.imageScale.toInt.tuple)
        cls.rect = cls.image.get_rect()
        cls.rect.center = cls.position.tuple
        cls.lastLevelUpTick = time.time()

    @classmethod
    def levelUp(cls):

        cls.level += 1
        cls.nextLevel += 1

        if cls.level >= cls.maxLevel:
            cls.radius = 2000
        else:
            cls.radius *= 1.5
        cls.lastLevelUpTick = GameTime.ticks

        cls.imageScale += 8
        cls.image = pygame.transform.scale(cls.image, cls.imageScale.toInt.tuple)
        cls.rect = cls.image.get_rect()
        cls.rect.center = cls.position.tuple

    @classmethod
    def canLevelUp(cls):
        if Camp.level == 1:
            if Camp.woodCount >= 10:
                return True
        elif Camp.level == 2:
            if Camp.woodCount >= 16:
                return True
        elif Camp.level == 3:
            if Camp.woodCount >= 26:
                return True
        elif Camp.level == 4:
            if Camp.woodCount >= 34:
                return True
        elif Camp.level == 5:
            if Camp.woodCount >= 58:
                return True

    @classmethod
    def canProduce(cls, buildingType: BuildingType):
        wood    = cls.woodCount
        swords  = cls.swordCount
        ingots  = cls.ironIngotCount
        ores    = cls.ironOreCount

        if buildingType == BuildingType.Mine:
            wood -= 10
        elif buildingType == BuildingType.Smith:
            wood -= 10
            ingots -= 3
        elif buildingType == BuildingType.Smelt:
            wood -= 10
        elif buildingType == BuildingType.TrainingCamp:
            wood -= 10

        return wood >= 0 and swords >= 0 and ingots >= 0 and ores >= 0
