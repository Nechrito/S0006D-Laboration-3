from typing import List

from src.Settings import SETTINGS
from src.code.ai.fsm.StateMachine import StateMachine
from src.code.engine.GameTime import GameTime
import random

from src.code.math.Vector import vec2
from src.code.pathfinding.Node import Node
from src.code.pathfinding.PathManager import PathManager
from src.enums.PathType import PathType


class Entity:

    waypoints: List[Node]

    def __init__(self, name, state, globalState, image, position):
        self.image = image
        self.name = name
        self.position = SETTINGS.closestNode(position).position

        self.rect = self.image.get_rect()
        self.rect.center = self.position.tuple

        self.waypoints = []

        self.pathfinder = PathManager(PathType.AStar)
        self.nextNode = self.position
        self.radius = 16

        self.fatigue = random.randrange(0, 70)
        self.bank = random.randrange(0, 120)
        self.thirst = random.randrange(0, 50)
        self.hunger = random.randrange(0, 50)

        self.setStart(self.position)

        if state is not None:
            self.stateMachine = StateMachine(self, state, globalState)
        else:
            self.stateMachine = None

    def updateState(self):
        self.thirst += 0.5 * GameTime.deltaTime
        self.hunger += 0.5 * GameTime.deltaTime
        self.fatigue += 0.5 * GameTime.deltaTime
        self.stateMachine.update()

    def update(self):

        self.rect = self.image.get_rect()
        self.rect.center = self.position.tuple

        if self.stateMachine is not None:
            self.updateState()

        if self.nextNode.distance(self.position) > self.radius:
            node = SETTINGS.closestNode(self.position, False)
            moveSpeed = 1.0
            if node:
                moveSpeed = node.moveSpeed
            self.position += (self.nextNode - self.position).normalized * GameTime.deltaTime * 200 * moveSpeed

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

        if len(temp) <= 1:
            targetNode = SETTINGS.closestNode(target, True, False)

            if not targetNode:
                return

            if not targetNode.isWalkable:
                for neighbour in targetNode.neighbours:
                    neighbourNode = SETTINGS.closestNode(neighbour, True, False)
                    if neighbourNode and neighbourNode.isWalkable:
                        temp = self.pathfinder.requestPathCached(self.waypoints, self.position, neighbourNode.position)

                if temp is None or len(temp) <= 1:
                    return

            else:
                temp = self.pathfinder.requestPathCached(self.waypoints, self.position, targetNode.position)

        if temp is None or len(temp) <= 1:
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