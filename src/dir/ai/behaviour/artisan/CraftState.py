from dir.engine.Camp import Camp
from dir.environment.Item import Item
from enums.ItemType import ItemType

from dir.ai.behaviour.IState import IState
from dir.ai.Message import Message


class CraftState(IState):
    def __init__(self):
        pass

    def enter(self, entity):
        Message.sendConsole(entity, "What to build today..")

    def execute(self, entity):
        pass

    def exit(self, entity):
        pass
