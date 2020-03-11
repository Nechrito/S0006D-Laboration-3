from debug.ai.behaviour.IState import IState
from debug.ai.Message import Message


class BuildingState(IState):
    def __init__(self):
        pass

    def enter(self, entity):
        Message.sendConsole(entity, "We could use some new buildings, I'll take care of it!")

    def execute(self, entity):
        #Todo: Build at camp
        pass

    def exit(self, entity):
        pass