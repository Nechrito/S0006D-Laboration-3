
from dir.engine.GameTime import GameTime
from src.dir.ai.Entity import SETTINGS
from dir.ai.behaviour.IState import IState
from dir.engine.Vars import Vars
from dir.ai.Message import Message
from dir.items.Wood import Wood


class WorkerState(IState):
    def __init__(self):
        self.isChoppingTree = False
        self.treeTarget = None
        self.itemTarget = None
        self.searchRadius = 16 * 4
        self.lastTick = 0
        self.tickThreshold = 500 # <- For sub-tasks, no need to check this each tick

    def enter(self, entity):
        Message.sendConsole(entity, "Sure could make use of more wood, will fetch some")

    def execute(self, entity):

        if self.itemTarget:
            if self.itemTarget.isPickedUp:

                entity.moveTo(Vars.campPosition)
                self.itemTarget.position = entity.position

                if entity.position.distance(Vars.campPosition) <= entity.radius:
                    Vars.itemsContainer.remove(self.itemTarget)
                    Vars.treeCount += 1
                    self.itemTarget = None
            else:
                entity.moveTo(self.itemTarget.position)
                if entity.position.distance(Vars.campPosition) <= 16:
                    self.itemTarget.isPickedUp = True
            return

        elif self.treeTarget:

            # busy chopping down tree
            if self.isChoppingTree:

                # update tree timer
                self.treeTarget.update()

                # if chopped, remove tree and swap into wood
                if self.treeTarget.isChopped and self.treeTarget in Vars.treesContainer:
                    Vars.treesContainer.remove(self.treeTarget)

                    wood = Wood(self.treeTarget.position)
                    Vars.itemsContainer.append(wood)

                    self.treeTarget = None
                    self.isChoppingTree = False
            else:
                # start tree timer if close, else move towards the tree
                distanceToTree = self.treeTarget.position.distance(entity.position)
                if distanceToTree <= entity.radius:
                    self.isChoppingTree = True
                    self.treeTarget.startTimer()
                else:
                    entity.moveTo(self.treeTarget.position)

        else:
            # locate items
            closestDistance = 0
            selectedItem = None
            # search the surrounding area for nearby items to pick up
            for item in Vars.itemsContainer:
                distanceToSub = item.position.distance(entity.position)

                if not item.isTarget and not item.isPickedUp and distanceToSub <= self.searchRadius and (closestDistance == 0 or distanceToSub < closestDistance):
                    closestDistance = distanceToSub
                    selectedItem = item
                    selectedItem.isPickedUp = True

            if selectedItem:
                self.itemTarget = selectedItem

            # find a tree to chop
            if not self.itemTarget:
                distToTree = 0
                for tree in Vars.treesContainer:
                    if tree.isChopped or tree.isTarget:
                        continue

                    if not SETTINGS.getNode(tree.position).isVisible:
                        continue

                    distTreeToEnt = tree.position.distance(entity.position)

                    if distTreeToEnt < distToTree or distToTree == 0:
                        self.treeTarget = tree
                        self.treeTarget.isTarget = True

    def exit(self, entity):
        pass
