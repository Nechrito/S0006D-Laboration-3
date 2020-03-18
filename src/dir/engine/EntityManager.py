from typing import List

from dir.ai.Entity import Entity
from dir.ai.Telegram import Telegram
from enums.EntityType import EntityType


class EntityManager:

    entities: List[Entity]

    @classmethod
    def init(cls):
        cls.entities = []

    @classmethod
    def register(cls, entity: Entity):
        cls.entities.append(entity)

    @classmethod
    def remove(cls, entity: Entity):
        cls.entities.remove(entity)

    @classmethod
    def getAllOfType(cls, entityType: EntityType):
        temp = []
        for entity in cls.entities:
            if entity.entityType == entityType:
                temp.append(entity)
        return temp

    @classmethod
    def sendMessage(cls, telegram: Telegram):
        for entity in EntityManager.entities:
            temp = telegram
            if temp.isForMe(entity):
                if not temp.target:
                    temp.target = entity
                entity.handleMessage(temp)

    @classmethod
    def update(cls):
        for entity in cls.entities:
            entity.update()

