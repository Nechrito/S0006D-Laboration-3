import time

from code.ai.behaviour.states.IState import IState
from code.engine.Vars import Vars
from code.ai.Message import Message


class WorkerState(IState):
    def __init__(self):
        self.isDoingWork = False
        self.primaryTarget = None
        self.subTargets = []
        self.searchRadius = 16 * 4
        self.lastTick = time.time()
        self.tickThreshold = 500

    def enter(self, entity):
        Message.sendConsole(entity, "Ok!")

    def execute(self, entity):
        if self.isDoingWork:
            return

        distanceToPrimary = 0
        if self.primaryTarget:
            distanceToPrimary = self.primaryTarget.position.distance(entity.position)


        closestDistance = 0
        selectedPrimary = None

        # limit the amount of sub-tasks checks
        currentTime = time.time()
        if currentTime - self.lastTick > self.tickThreshold:
            self.lastTick = currentTime

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
            self.primaryTarget = selectedPrimary

    def exit(self, entity):
        pass
