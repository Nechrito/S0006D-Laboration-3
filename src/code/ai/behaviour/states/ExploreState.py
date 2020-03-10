from Settings import SETTINGS
from code.ai.behaviour.states.IState import IState
from src.code.ai.messaging.Message import Message


class ExploreState(IState):
    def __init__(self):
        self.currentTarget = None

    def enter(self, entity):
        Message.sendConsole(entity, "Guess I'll explore the world!")

    def execute(self, entity):
        if self.currentTarget and self.currentTarget.position.distance(entity.position) > entity.radius:
            return

        nearestNode = SETTINGS.getClosestFOWNode(entity.position)
        if nearestNode:
            print("?")

            if nearestNode is not self.currentTarget:
                self.currentTarget = nearestNode
                Message.sendConsole(entity, "Got me a new destination")
            entity.moveTo(self.currentTarget.position)

    def exit(self, entity):
        pass
