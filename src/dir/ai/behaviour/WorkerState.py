import time

from dir.ai.behaviour.IState import IState
from dir.engine.Vars import Vars
from dir.ai.Message import Message
from dir.items.Wood import Wood


class WorkerState(IState):
    def __init__(self):
        self.isDoingWork = False
        self.primaryTarget = None
        self.targetPos = None
        self.subTargets = []
        self.searchRadius = 16 * 4
        self.lastTick = 0
        self.tickThreshold = 500

    def enter(self, entity):
        Message.sendConsole(entity, "Sure could make use of more wood, will fetch some")

    def execute(self, entity):

        if self.primaryTarget:
            self.primaryTarget.update()

        if self.isDoingWork:
            if self.primaryTarget.isChopped:
                Vars.treesContainer.remove(self.primaryTarget)

                wood = Wood(self.targetPos)
                Vars.itemsContainer.append(wood)

                self.primaryTarget = None
                self.isDoingWork = False
            else:
                return

        distanceToPrimary = 0
        if self.primaryTarget:

            distanceToPrimary = self.targetPos.distance(entity.position)
            if self.targetPos.distance(entity.position) <= entity.radius:
                self.isDoingWork = True
                self.primaryTarget.startTimer()
            else:
                entity.moveTo(self.targetPos)

        selectedPrimary = None

        # limit the amount of sub-tasks checks
        currentTime = time.time()
        if currentTime - self.lastTick >= self.tickThreshold or self.lastTick == 0:
            self.lastTick = currentTime
            closestDistance = 0

            for item in Vars.itemsContainer:
                if self.primaryTarget:
                    distanceToSub = item.position.distance(entity.position)

                    if self.primaryTarget:
                        if item not in self.subTargets and distanceToSub <= self.searchRadius and distanceToSub < distanceToPrimary:
                            self.subTargets.append(item)

                        if item in self.subTargets and distanceToSub > self.searchRadius:
                            self.subTargets.remove(item)
                    else:
                        if closestDistance == 0 or distanceToSub < closestDistance:
                            closestDistance = distanceToSub
                            selectedPrimary = item

        if not self.primaryTarget:
            if selectedPrimary:
                self.primaryTarget = selectedPrimary
            else:
                distToTree = 0
                selectedTree = None
                for tree in Vars.treesContainer:
                    cachedDist = tree.position.distance(entity.position)
                    if cachedDist < distToTree and cachedDist <= 300 or distToTree == 0:
                        selectedTree = tree
                        distToTree = cachedDist

                if selectedTree:
                    self.primaryTarget = selectedTree
                    self.targetPos = self.primaryTarget.position

    def exit(self, entity):
        pass
