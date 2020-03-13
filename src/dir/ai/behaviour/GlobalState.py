from enums.EntityType import EntityType
from src.dir.ai.Entity import Entity
from dir.ai.behaviour.IState import IState
from src.dir.engine.GameTime import GameTime


class GlobalState(IState):

    def __init__(self):
        self.currentState = None
        self.lastTick = GameTime.ticks

    def enter(self, entity: Entity):
        pass

    def execute(self, entity: Entity):
        if GameTime.timeSince(self.lastTick) < GameTime.relativeDuration(1):
            return

        self.lastTick = GameTime.ticks

    def exit(self, entity: Entity):
        pass
