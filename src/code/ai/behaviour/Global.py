from src.code.ai.Entity import Entity
from src.code.ai.behaviour.IState import IState
from src.code.ai.behaviour.states.DrinkingState import Drink
from src.code.ai.behaviour.states.SleepingState import Sleep
from src.code.ai.behaviour.states.CollectState import Collect
from src.code.ai.behaviour.states.EatingState import Eat
from src.code.engine.GameTime import GameTime


class Global(IState):

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

        if entity.hunger >= 95 and not self.currentState == Eat:
            #self.cachedCondition = self.memoize(entity.hunger <= 5)
            self.currentState = Eat
            entity.setState(Eat(), True)

        if entity.fatigue >= 95 and not self.currentState == Sleep:
            #self.cachedCondition = self.memoize(entity.fatigue <= 5)
            self.currentState = Sleep
            entity.setState(Sleep(), True)

        if entity.thirst >= 95 and not self.currentState == Drink:
            #self.cachedCondition = self.memoize(entity.thirst <= 5)
            self.currentState = Drink
            entity.setState(Drink(), True)

        if entity.bank <= 10 and not self.currentState == Collect:
            #self.cachedCondition = self.memoize(entity.bank >= 30)
            self.currentState = Collect
            entity.setState(Collect(), True)

    def exit(self, entity: Entity):
        pass
