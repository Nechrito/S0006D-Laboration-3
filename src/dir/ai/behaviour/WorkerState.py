import time

from src.dir.ai.Entity import SETTINGS
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
        self.tickThreshold = 500 # <- For sub-tasks, no need to check this each tick

    def enter(self, entity):
        Message.sendConsole(entity, "Sure could make use of more wood, will fetch some")

    def execute(self, entity):

        # update tree timer
        if self.primaryTarget:
            self.primaryTarget.update()

        # busy chopping down tree
        if self.isDoingWork:

            # if chopped, remove tree and swap into wood
            if self.primaryTarget.isChopped and self.primaryTarget in Vars.treesContainer:
                Vars.treesContainer.remove(self.primaryTarget)

                wood = Wood(self.targetPos)
                Vars.itemsContainer.append(wood)

                self.primaryTarget = None
                self.isDoingWork = False
            else: # no need to continue loop if tree timer isn't completed
                return

        # walk towards selected tree, if any
        if self.primaryTarget:

            # start tree timer if close, else move towards the tree
            distanceToPrimary = self.targetPos.distance(entity.position)
            if distanceToPrimary <= entity.radius:
                self.isDoingWork = True
                self.primaryTarget.startTimer()
            else:
                entity.moveTo(self.targetPos)

        # sub-tasks if within timeframe
        selectedPrimary = None
        currentTime = time.time()
        if currentTime - self.lastTick >= self.tickThreshold or self.lastTick == 0:
            self.lastTick = currentTime
            closestDistance = 0

            # search the surrounding area for nearby items to pick up
            for item in Vars.itemsContainer:
                distanceToSub = item.position.distance(entity.position)

                if not item.isTarget and distanceToSub <= self.searchRadius and (closestDistance == 0 or distanceToSub < closestDistance):
                    closestDistance = distanceToSub
                    selectedPrimary = item
                    selectedPrimary.isTarget = True

        # find a new primary task
        if not self.primaryTarget:
            # if we've located an item, then select it
            if selectedPrimary:
                self.primaryTarget = selectedPrimary
            else:
                # locate a nearby tree to chop down
                distToTree = 0
                selectedTree = None
                for tree in Vars.treesContainer:
                    if tree.isChopped or tree.isTarget:
                        continue

                    if not SETTINGS.getNode(tree.position).isVisible:
                        continue

                    distTreeToEnt = tree.position.distance(entity.position)
                    distTreeToCamp = tree.position.distance(Vars.campPosition)

                    if distTreeToEnt < distToTree or distToTree == 0:
                        selectedTree = tree
                        selectedTree.isTarget = True
                        distToTree = distTreeToEnt

                if selectedTree:
                    selectedTree.isTarget = True
                    self.primaryTarget = selectedTree
                    self.targetPos = self.primaryTarget.position

    def exit(self, entity):
        pass
