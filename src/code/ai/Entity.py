import random

from enums.EntityType import EntityType
from src.Settings import *
from code.ai.StateMachine import StateMachine
from src.code.engine.GameTime import GameTime
from src.code.math.Vector import vec2
from src.code.pathfinding.PathManager import PathManager
from src.enums.PathType import PathType


class Entity:

    def __init__(self, characterType: EntityType, position, image, startState, globalState):
        self.characterType = characterType
        self.stateMachine = StateMachine(self, startState, globalState)
        self.position = position
        self.image = image
        self.name = str(characterType).replace("EntityType.", "")
        self.moveSpeed = random.randrange(75, 150)

        self.rect = self.image.get_rect()
        self.rect.center = self.position.tuple

        self.waypoints = []

        self.pathfinder = PathManager(PathType.AStar)
        self.nextNode = self.position
        self.radius = 16

        self.setStart(self.position)

    def update(self):

        self.stateMachine.update()

        self.rect = self.image.get_rect()
        self.rect.center = self.position.tuple

        if self.nextNode.distance(self.position) > self.radius:
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
        if target.distance(self.position) <= self.radius:
            return

        temp = self.pathfinder.requestPathCached(self.waypoints, self.position, target)
        if temp is None:
            return

        if len(temp) <= 2:
            targetNode = SETTINGS.getNode(target, False, False)

            if not targetNode:
                return

            if not targetNode.isWalkable:
                for neighbour in targetNode.neighbours:
                    neighbourNode = SETTINGS.getNode(neighbour, False, False)
                    if neighbourNode and neighbourNode.isWalkable:
                        temp = self.pathfinder.requestPathCached(self.waypoints, self.position, neighbourNode.position)

                if temp is None or len(temp) <= 2:
                    return

            else:
                temp = self.pathfinder.requestPathCached(self.waypoints, self.position, targetNode.position)

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