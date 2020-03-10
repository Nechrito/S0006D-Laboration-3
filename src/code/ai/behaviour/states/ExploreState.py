from Settings import SETTINGS
from code.ai.behaviour.states.IState import IState
from src.code.ai.messaging.Message import Message


class ExploreState(IState):

    def __init__(self):
        self.currentTarget = None

    def enter(self, entity):
        Message.sendConsole(entity, "Guess I'll explore the world!")
        self.currentTarget = SETTINGS.getClosestFOWNode(entity.position)

    def execute(self, entity):
        if self.currentTarget:
            entity.moveTo(self.currentTarget.position)

            if self.currentTarget.position.distance(entity.position) > entity.radius:
                return

        nearestNode = SETTINGS.getClosestFOWNode(entity.position)
        if nearestNode:
            print("1")

            if nearestNode is not self.currentTarget:
                self.currentTarget = nearestNode
                Message.sendConsole(entity, "Got me a new destination")

    def exit(self, entity):
        pass
