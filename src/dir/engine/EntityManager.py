from typing import List

from dir.ai.Entity import Entity
from dir.ai.Telegram import Telegram
from dir.ai.behaviour.generic.GlobalState import GlobalState
from dir.ai.behaviour.generic.IdleState import IdleState
from enums.EntityType import EntityType
from enums.MessageType import MessageType


class EntityManager:

    imgHatguy = None
    imgSensei = None
    campPosition = None
    entities: List[Entity]

    @classmethod
    def init(cls, campPos, imageHatguy, imageSensei):
        cls.entities = []
        cls.campPosition = campPos
        cls.imgHatguy = imageHatguy
        cls.imgSensei = imageSensei

    @classmethod
    def register(cls, entityType: EntityType):
        if entityType == EntityType.Explorer:
            img = cls.imgSensei
        elif entityType == EntityType.Worker:
            img = cls.imgHatguy
        else: # todo: if we want more images
            img = cls.imgHatguy

        entity = Entity(entityType, cls.campPosition, img, IdleState(), GlobalState())
        cls.entities.append(entity)
        cls.sendMessage(Telegram(messageType=MessageType.StateChange, target=entity))

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
        for entity in cls.entities:
            temp = telegram
            if temp.isForMe(entity) or temp.entityType == EntityType.Ignored:
                if not temp.target:
                    temp.target = entity
                entity.handleMessage(temp)

    @classmethod
    def update(cls):
        for entity in cls.entities:
            entity.update()

