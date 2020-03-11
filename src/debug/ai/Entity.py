import random

from enums.EntityType import EntityType
from src.Settings import *
from debug.ai.StateMachine import StateMachine
from src.debug.engine.GameTime import GameTime
from src.debug.math.Vector import vec2
from src.debug.pathfinding.PathManager import PathManager
from src.enums.PathType import PathType


class Entity:

    def __init__(self, characterType: EntityType, position, image, startState, globalState):
        self.characterType = characterType
        self.stateMachine = StateMachine(self, startState, globalState)
        self.position = position
        self.image = image
        self.name = str(characterType).replace("EntityType.", "")
        self.moveSpeed = random.randrange(30, 50)

        self.rect = self.image.get_rect()
        self.rect.center = self.position.tuple

        self.waypoints = []

        self.pathfinder = PathManager(PathType.AStar)
        self.nextNode = self.position
        self.radius = 8

        self.setStart(self.position)

    def update(self):

        self.stateMachine.update()

        self.rect = self.image.get_rect()
        self.rect.center = self.position.tuple

        if self.nextNode.distance(self.position) >= 4:
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

        temp = self.pathfinder.requestPathCached(self.waypoints, self.position, target)
        if not temp or len(temp) <= 1:
            temp = self.pathfinder.requestPathCached(self.waypoints, self.position.randomized(4), target)

        if not temp:
            return

        if not temp or len(temp) <= 1:
            return

        self.waypoints = temp
        self.nextNode = self.waypoints[1].position

    def setStart(self, start: vec2, end: vec2 = None):
        self.waypoints = []
        self.position = start

        self.rect = self.image.get_rect()
        self.rect.center = self.position.tuple

        if end:
            temp = self.pathfinder.requestPath(start, end)
            if temp is None:
                return

            self.waypoints = temp
            self.nextNode = self.waypoints[1].position

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