from debug.ai.behaviour.IState import IState
from debug.ai.Message import Message


class TreeState(IState):
    def __init__(self):
        pass

    def enter(self, entity):
        Message.sendConsole(entity, "Sure could make use of more wood, will fetch some")

    def execute(self, entity):
        pass

    def exit(self, entity):
        pass