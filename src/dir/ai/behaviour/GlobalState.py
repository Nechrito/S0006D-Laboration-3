import random
import time

from dir.ai.behaviour.artisan.CraftState import CraftState
from dir.ai.behaviour.artisan.MineState import MineState
from dir.ai.behaviour.artisan.SmeltState import SmeltState
from dir.ai.behaviour.artisan.SmithState import SmithState
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
        self.lastTick = GameTime.ticks
        pass

    def exit(self, entity: Entity):
        pass
