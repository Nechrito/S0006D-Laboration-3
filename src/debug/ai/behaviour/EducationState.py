from debug.ai.behaviour.IState import IState
from debug.ai.Message import Message


class EducationState(IState):
    def __init__(self):
        pass

    def enter(self, entity):
        Message.sendConsole(entity, "Need to educate myself some more")

    def execute(self, entity):
        pass

    def exit(self, entity):
        pass
