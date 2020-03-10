from code.ai.behaviour.states.IState import IState
from src.code.ai.messaging.Message import Message


class WorkerState(IState):
    def __init__(self):
        self.isDoingWork = False

    def enter(self, entity):
        Message.sendConsole(entity, "Ok!")

    def execute(self, entity):


    def exit(self, entity):
        pass
