import random
import time

from dir.ai.StateMachine import StateMachine
from enums.EntityType import EntityType
from src.Settings import *
from src.dir.engine.GameTime import GameTime
from src.dir.math.Vector import vec2
from src.dir.pathfinding.PathManager import PathManager
from src.enums.PathType import PathType


class Entity:

    def __init__(self, entityType: EntityType, campPos, image, startState, globalState):
        self.entityType = entityType
        self.name = str(entityType).replace("EntityType.", "")
        self.stateMachine = StateMachine(self, startState, globalState)
        self.position = campPos.randomized(9)
        self.image = image
        self.moveSpeed = random.randrange(20, 35)
        self.createdTime = time.time()
        self.isComputingPath = False

        # increase movement speed by 20% if entity is an explorer
        if entityType == EntityType.Explorer:
            self.moveSpeed *= 1.20

        self.rect = self.image.get_rect()
        self.rect.center = self.position.tuple
        self.scaleTime = GameTime.timeScale
        self.isBeingUpgraded = False

        self.pathfinder = PathManager(PathType.AStar)
        self.waypoints = []
        self.nextNode = self.position

        self.radius = 16

    def update(self):
        self.scaleTime = GameTime.timeScale

        self.stateMachine.update()

        self.rect.center = self.position.tuple

        if self.isComputingPath:
            return

        if self.nextNode.distance(self.position) >= self.radius:
            node = SETTINGS.getNode(self.position, True, False)
            moveSpeedMultiplier = 1.0
            if node:
                moveSpeedMultiplier = node.moveSpeed
            self.position += (self.nextNode - self.position).normalized * self.moveSpeed * GameTime.deltaTime * moveSpeedMultiplier

        elif len(self.waypoints) >= 2:
            self.waypoints.pop(0)
            if len(self.waypoints) >= 2:
                self.nextNode = self.waypoints[1].position

    def moveTo(self, target: vec2):
        self.isComputingPath = True
        temp = self.pathfinder.requestPathCached(self.waypoints, self.position, target)
        if not temp or len(temp) <= 1:
            return

        self.isComputingPath = False
        self.waypoints = temp
        self.nextNode = self.waypoints[1].position

    def handleMessage(self, telegram):
        self.stateMachine.handleMessage(telegram)

    def setState(self, state):
        self.stateMachine.change(state)

    def revertState(self):
        self.stateMachine.revert()

    def getPathType(self):
        return self.pathfinder.getPathType()

    def setPathType(self, pathType):
        self.pathfinder = PathManager(pathType)

    def isCloseTo(self, to: vec2):
        return self.position.distance(to) <= self.radius