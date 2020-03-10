from code.ai.behaviour.states.IState import IState
from src.code.ai.messaging.Message import Message


class TreeState(IState):
    def __init__(self):
        pass

    def enter(self, entity):
        Message.sendConsole(entity, "Sure could make use of more wood, will fetch some")

    def execute(self, entity):
        pass

    def exit(self, entity):
        pass
