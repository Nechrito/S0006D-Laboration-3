import random
import time

from Game import Camp
from dir.ai.Message import Message
from dir.ai.StateTransition import StateTransition
from dir.ai.Telegram import Telegram
from dir.ai.behaviour.IState import IState
from dir.engine.EntityManager import EntityManager
from enums.EntityType import EntityType
from enums.MessageType import MessageType
from enums.StateType import StateType
from src.dir.ai.Entity import SETTINGS


class ExploreState(IState):

    def __init__(self):
        self.currentTarget = None
        self.avoidableTarget = None
        self.entity = None
        self.lastCheckTick = 0
        self.moveRate = 0
        self.threshold = 0.65

    def enter(self, entity):
        self.entity = entity
        Message.sendConsole(entity, "Guess I'll do some explorin' ")

    def handleMessage(self, telegram):
        if self.entity and telegram.source != self.entity and telegram.isMyType(self.entity):
            if telegram.messageType == MessageType.PositionChange:
                self.avoidableTarget = telegram.message

               # if self.currentTarget and self.currentTarget.distance(self.avoidableTarget) < Camp.radius * self.threshold:
                    #self.currentTarget = None

    def execute(self, entity):

        if self.currentTarget:
            entity.moveTo(self.currentTarget)

            if self.currentTarget.distance(entity.position) <= entity.radius:
                self.currentTarget = None

        elif time.time() - self.lastCheckTick >= self.moveRate: # seconds
            self.lastCheckTick = time.time()
            temp = self.getUnmarkedNode(entity)
            if temp:
                self.currentTarget = temp
            else:
                return
            self.avoidableTarget = None
            self.moveRate = random.randrange(250, 750) / 1000

            if self.currentTarget:
                # let all other Explorers know where I'm headed, so they don't walk there aswell
                EntityManager.sendMessage(Telegram(source=entity, entityType=EntityType.Explorer, messageType=MessageType.PositionChange, message=self.currentTarget))
            else:
                Message.sendConsole(entity, "Hm.. nothing to do huh")
                StateTransition.setState(entity, StateType.IdleState)

    def getUnmarkedNode(self, entity):

        # shouldn't be much of a difference anyway
        closest = (self.currentTarget if self.currentTarget else SETTINGS.getNode(entity.position))
        distance = 0
        for i in SETTINGS.Graph:
            for node in i:
                # Could perform class type Node check, but might result in circular import
                # this is fine though, Graph wont contain anything else
                if not node or node.isVisible or not node.isWalkable:
                    continue

                currentDist = node.position.distance(Camp.position)
                if currentDist <= Camp.radius:
                    if currentDist > distance != 0:
                        continue

                    if self.avoidableTarget:
                        if self.avoidableTarget.distance(node.position)  * self.threshold <= entity.position.distance(node.position):
                            continue

                    distance = currentDist
                    closest = node

        if closest:
            return closest.position
        else:
            StateTransition.setState(entity, StateType.IdleState)

    def exit(self, entity):
        pass
