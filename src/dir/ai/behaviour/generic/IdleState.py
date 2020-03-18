import random
import time

from dir.ai.behaviour.IState import IState
from dir.environment.Camp import Camp


class IdleState(IState):
    def __init__(self):
        self.lastMoveTick = 0
        self.moveTickMin = 1000
        self.moveTickMax = 3000
        self.moveRate = random.randint(self.moveTickMin, self.moveTickMax)
        self.destination = None

    def enter(self, entity):
        self.entity = entity

    def handleMessage(self, telegram):
        pass

    def execute(self, entity):

        if not self.destination or (self.destination and self.destination.distance(entity.position) <= entity.radius):
            self.lastMoveTick = time.time()
            self.moveRate = random.randint(self.moveTickMin, self.moveTickMax)
            self.destination = Camp.position.randomized(maxDist=10, minDist=5)

        # move around once in a while
        if self.destination and time.time() - self.lastMoveTick > self.moveRate / 1000:
            entity.moveTo(self.destination)

    def exit(self, entity):
        pass
