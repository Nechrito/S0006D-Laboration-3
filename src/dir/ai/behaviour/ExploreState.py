import time

from dir.ai.behaviour.IState import IState
from dir.ai.Message import Message
from dir.engine.Vars import Vars
from src.dir.ai.Entity import SETTINGS, DynamicGraph


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

        if self.currentTarget and self.currentTarget.position:
            entity.moveTo(self.currentTarget.position)

            if self.currentTarget.position.distance(entity.position) > entity.radius:
                return

        nearestNode = self.getClosestFOWNode(entity.position, Vars.campPosition, Vars.campRadius)
        if nearestNode and nearestNode is not self.currentTarget:
            self.currentTarget = nearestNode
            self.isIdle = False
        else:
            self.isIdle = True
            Message.sendConsole(entity, "Done exploring, for now")

    def getClosestFOWNode(self, position, camp, maxRange=100):
        closest = None
        distance = 0

        for i in SETTINGS.Graph:
            for j in i:

                # Could perform class type Node check, but might result in circular import
                # this is fine though, Graph wont contain anything else
                if type(j) == DynamicGraph or j.isVisible or not j.isWalkable:
                    continue

                if j.position.distance(camp) > maxRange:
                    continue

                currentDist = j.position.distance(position)

                if 16 * 3 <= currentDist < distance or distance == 0:
                    distance = currentDist
                    closest = j
        return closest

    def exit(self, entity):
        pass
