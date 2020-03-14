from dir.engine.Camp import Camp
from dir.environment.Item import Item
from enums.EntityType import EntityType
from enums.ItemType import ItemType

from dir.ai.behaviour.IState import IState
from dir.ai.Message import Message


class CraftState(IState):
    def __init__(self):
        pass

    def enter(self, entity):
        entity.setType(EntityType.Craftsman)
        Message.sendConsole(entity, "What to build today..") # (training camps lol)

    def execute(self, entity):
        pass

    def exit(self, entity):
        pass
