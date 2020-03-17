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
from src.dir.ai.Entity import SETTINGS, DynamicGraph


class ExploreState(IState):

    def __init__(self):
        self.currentTarget = None
        self.avoidableTarget = None
        self.source = None
        self.lastCheckTick = 0
        self.moveRate = 0
        self.threshold = 0.15

        #self.pool = ThreadPool(processes=1)
        #self.async_result = None

    def enter(self, entity):
        self.source = entity
        Message.sendConsole(entity, "Guess I'll explore the world!")

    def handleMessage(self, telegram):
        if self.source and telegram.source != self.source:
            self.avoidableTarget = telegram.message

            if self.currentTarget and self.currentTarget.distance(self.avoidableTarget) <= Camp.radius * self.threshold:
                self.currentTarget = None

    def execute(self, entity):

        if self.currentTarget:
            entity.moveTo(self.currentTarget)

            if self.currentTarget.distance(entity.position) <= entity.radius:
                self.currentTarget = None

        elif time.time() - self.lastCheckTick >= self.moveRate: # seconds
            self.lastCheckTick = time.time()
            #self.getUnmarkedNode(entity)
            self.avoidableTarget = None
            self.moveRate = random.randrange(250, 750) / 1000

            # let all other Explorers know where I'm headed, so they don't walk there aswell
            EntityManager.sendMessage(Telegram(entity, EntityType.Explorer, MessageType.PositionChange, self.currentTarget))

    def getUnmarkedNode(self, entity):

        closest = None
        distance = 0
        for i in SETTINGS.Graph:
            for node in i:
                # Could perform class type Node check, but might result in circular import
                # this is fine though, Graph wont contain anything else
                if node is None or not node or type(node) == DynamicGraph or node.isVisible or not node.isWalkable:
                    continue

                currentDist = node.position.distance(Camp.position)
                if currentDist < Camp.radius or closest is None:
                    if currentDist > distance != 0:
                        continue

                    if self.avoidableTarget:
                        if self.avoidableTarget.distance(node.position) < Camp.radius * self.threshold:
                            continue

                    distance = currentDist
                    closest = node

        if closest:
            self.currentTarget = closest.position
        else:
            StateTransition.setState(entity, StateType.IdleState)

    def exit(self, entity):
        pass
