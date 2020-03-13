from dir.ai.StateTransition import StateTransition
from dir.ai.behaviour.IState import IState
from dir.ai.Message import Message
from enums.StateType import StateType
from src.dir.ai.Entity import SETTINGS, DynamicGraph
from Game import Camp


class ExploreState(IState):

    def __init__(self):
        self.currentTarget = None

    def enter(self, entity):
        Message.sendConsole(entity, "Guess I'll explore the world!")

    def execute(self, entity):

        if self.currentTarget:
            entity.moveTo(self.currentTarget)

            if self.currentTarget.distance(entity.position) <= entity.radius:
                self.currentTarget = None
        else:
            nearestNode = self.getUnmarkedNode()
            if nearestNode:
                self.currentTarget = nearestNode.position.randomized()
            else:
                StateTransition.setState(entity, StateType.IdleState)

    def getUnmarkedNode(self):
        closest = None
        distance = 0

        for i in SETTINGS.Graph:
            for j in i:

                # Could perform class type Node check, but might result in circular import
                # this is fine though, Graph wont contain anything else
                if type(j) == DynamicGraph or j.isVisible or not j.isWalkable:
                    continue

                if j.position.distance(Camp.position) > Camp.radius:
                    continue

                currentDist = j.position.distance(Camp.position)

                # the min check makes sure multiple explorers don't trace after eachother
                if 16 * 4 <= currentDist < distance or distance == 0:
                    distance = currentDist
                    closest = j

        return closest

    def exit(self, entity):
        pass
