from dir.ai.behaviour.IState import IState
from src.dir.ai.Entity import Entity
from src.dir.engine.GameTime import GameTime


class GlobalState(IState):

    def __init__(self):
        self.currentState = None
        self.lastTick = GameTime.ticks

    def enter(self, entity: Entity):
        pass

    def handleMessage(self, telegram):
        pass

    def execute(self, entity: Entity):
        self.lastTick = GameTime.ticks
        pass

    def exit(self, entity: Entity):
        pass
