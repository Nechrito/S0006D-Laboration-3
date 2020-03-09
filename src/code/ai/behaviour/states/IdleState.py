from src.code.ai.behaviour.IState import IState
from src.code.ai.messaging.Message import Message


class IdleState(IState):
    def __init__(self):
        pass

    def enter(self, entity):
        Message.sendConsole(entity, "Nothing to do...")

    def execute(self, entity):
        pass

    def exit(self, entity):
        pass
