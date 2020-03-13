import pygame

from typing import List

from dir.engine.GameTime import GameTime
from dir.environment.Item import Item
from dir.environment.Tree import Tree
from dir.math.Vector import vec2


class Camp:

    level = 1
    radius = 200
    position: vec2 = None
    image: pygame.Surface
    rect: pygame.Rect

    lastLevelUpTick = 0

    woodCount      = 0
    charcoalCount  = 0
    ironIngotCount = 0
    ironOreCount   = 0
    swordCount     = 0
    soldierCount   = 0

    # contains all items which may be picked up
    itemsContainer:  List[Item] = []
    treesContainer:  List[Tree] = []

    @classmethod
    def init(cls, campPos: vec2, image):
        cls.position = campPos
        cls.image = image
        cls.rect = cls.image.get_rect()
        cls.rect.center = cls.position.tuple
        cls.lastLevelUpTick = GameTime.ticks

    @classmethod
    def levelUp(cls, entities):
        cls.level += 1
        cls.radius *= 3
        cls.lastLevelUpTick = GameTime.ticks

        #for entity in entities:
        #    if entity.characterType == EntityType.Explorer:
        #        StateTransition.setState(entity, StateType.ExploreState)

    @classmethod
    def canProduceCharcoal(cls):
        return cls.woodCount >= 2

    @classmethod
    def canProduceIronIngot(cls):
        return cls.ironOreCount >= 2 and cls.charcoalCount >= 3

    @classmethod
    def canProduceSword(cls):
        return cls.ironIngotCount >= 1 and cls.charcoalCount >= 2


