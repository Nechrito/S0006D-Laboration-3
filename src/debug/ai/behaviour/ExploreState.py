import time

from debug.ai.behaviour.IState import IState
from debug.ai.Message import Message
from debug.engine.Vars import Vars
from src.debug.ai.Entity import SETTINGS


class ExploreState(IState):

    def __init__(self):
        self.currentTarget = None
        self.isIdle = False
        self.lastTick = 0
        self.threshold = 1000

    def enter(self, entity):
        Message.sendConsole(entity, "Guess I'll explore the world!")

    def execute(self, entity):
        if self.isIdle:
            if time.time() - self.lastTick < self.threshold:
                return
            self.lastTick = time.time()

        if self.currentTarget:
            entity.moveTo(self.currentTarget.position)

            if self.currentTarget.position.distance(entity.position) > entity.radius:
                return

        nearestNode = SETTINGS.getClosestFOWNode(entity.position, Vars.campPosition, Vars.campRadius)
        if nearestNode:
            if nearestNode is not self.currentTarget:
                self.currentTarget = nearestNode
                #Message.sendConsole(entity, "Got me a new destination")
                self.isIdle = False
        else:
            self.isIdle = True
            Message.sendConsole(entity, "Done exploring, for now")

    def exit(self, entity):
        pass
