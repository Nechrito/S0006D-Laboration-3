from src.code.ai.behaviour.IState import IState
from src.code.ai.messaging.Message import Message


class ExploreState(IState):
    def __init__(self):
        pass

    def enter(self, entity):
        Message.sendConsole(entity, "Guess I'll explore the world!")

    def execute(self, entity):
        pass

    def exit(self, entity):
        pass
