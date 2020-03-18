from dir.ai.behaviour.IState import IState
from src.dir.ai.Entity import Entity


class GlobalState(IState):

    def __init__(self):
        self.entity = None

    def enter(self, entity: Entity):
        self.entity = entity

    def handleMessage(self, telegram):
        pass

    def execute(self, entity: Entity):
        pass

    def exit(self, entity: Entity):
        pass
