from src.debug.ai.Entity import Entity
from debug.ai.behaviour.IState import IState
from src.debug.engine.GameTime import GameTime


class GlobalState(IState):

    def __init__(self):
        self.currentState = None
        self.lastTick = GameTime.ticks

    def __repr__(self):
        pass

    def enter(self, entity: Entity):
        pass

    def execute(self, entity: Entity):
        if GameTime.ticks - self.lastTick < GameTime.minutesToMilliseconds(0.1):
            return

        self.lastTick = GameTime.ticks

    def exit(self, entity: Entity):
        pass
