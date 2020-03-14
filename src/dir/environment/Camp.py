import time

import pygame

from typing import List

from dir.ai.StateTransition import StateTransition
from dir.engine.GameTime import GameTime
from dir.environment.Item import Item
from dir.environment.Mine import Mine
from dir.environment.Smelting import Smelting
from dir.environment.Smith import Smith
from dir.environment.Training import TrainingCamp
from dir.environment.Tree import Tree
from dir.math.Vector import vec2
from enums.EntityType import EntityType
from enums.StateType import StateType


class Camp:

    level = 1
    radius = 300
    position: vec2
    image: pygame.Surface
    imageScale: vec2
    rect: pygame.Rect

    lastLevelUpTick = 0

    woodCount      = 0
    charcoalCount  = 0
    ironIngotCount = 0
    ironOreCount   = 0
    swordCount     = 0
    soldierCount   = 0

    # contains all items which may be picked up
    itemsContainer: List[Item] = []
    treesContainer: List[Tree] = []

    # complexes which may be used by artisans
    mines:             List[Mine]         = []
    smithComplexes:    List[Smith]        = []
    smeltingComplexes: List[Smelting]     = []
    trainingCamps:     List[TrainingCamp] = []

    @classmethod
    def init(cls, campPos: vec2, image):
        cls.position = campPos
        cls.imageScale = vec2(32, 32)
        cls.image = image
        cls.rect = cls.image.get_rect()
        cls.rect.center = cls.position.tuple
        cls.lastLevelUpTick = time.time()

    @classmethod
    def levelUp(cls, entities):
        cls.level += 1
        cls.radius *= 1.25
        cls.lastLevelUpTick = GameTime.ticks
        cls.imageScale = vec2(32, 32) * (cls.level + 0.5)
        cls.image = pygame.transform.scale(cls.image, cls.imageScale.toInt.tuple)
        cls.rect = cls.image.get_rect()
        cls.rect.center = cls.position.tuple

        for entity in entities:
            if entity.entityType == EntityType.Explorer:
                StateTransition.setState(entity, StateType.ExploreState)

    @classmethod
    def canProduceCharcoal(cls):
        return cls.woodCount >= 2

    @classmethod
    def canProduceIronIngot(cls):
        return cls.ironOreCount >= 2 and cls.charcoalCount >= 3

    @classmethod
    def canProduceSword(cls):
        return cls.ironIngotCount >= 1 and cls.charcoalCount >= 2


