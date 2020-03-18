import random
import time

from dir.ai.StateTransition import StateTransition
from dir.ai.behaviour.IState import IState
from dir.environment.Camp import Camp
from enums.EntityType import EntityType
from enums.MessageType import MessageType
from enums.StateType import StateType


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
        if not self.entity:
            if telegram.target:
                self.entity = telegram.target
            else:
                return
        if telegram.messageType == MessageType.RevertState:
            self.entity.revertState()
        elif telegram.messageType == MessageType.StateChange:

            if self.entity.entityType == EntityType.Worker:
                StateTransition.setState(self.entity, StateType.WorkState)

            elif self.entity.entityType == EntityType.Explorer:
                StateTransition.setState(self.entity, StateType.ExploreState)

            elif self.entity.entityType == EntityType.Miner:
                StateTransition.setState(self.entity, StateType.ArtisanMiner)

            elif self.entity.entityType == EntityType.Craftsman:
                StateTransition.setState(self.entity, StateType.ArtisanCraftsman)

            elif self.entity.entityType == EntityType.Smelter:
                StateTransition.setState(self.entity, StateType.ArtisanSmelter)

            elif self.entity.entityType == EntityType.Smith:
                StateTransition.setState(self.entity, StateType.ArtisanSmith)

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
