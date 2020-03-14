import threading

from dir.engine.Camp import Camp
from dir.environment.Item import Item
from enums.ItemType import ItemType

from src.dir.ai.Entity import SETTINGS
from dir.ai.behaviour.IState import IState
from dir.ai.Message import Message


class WorkerState(IState):
    def __init__(self):
        self.isChoppingTree = False
        self.treeTarget = None
        self.itemTarget = None
        self.searchRadius = 16 * 4

    def enter(self, entity):
        Message.sendConsole(entity, "Sure could make use of more wood, will fetch some")

    def execute(self, entity):

        if self.itemTarget:
            if self.itemTarget.isPickedUp:
                t = threading.Thread(target=entity.moveTo, args=(Camp.position,))
                t.start()

                self.itemTarget.position = entity.position

                if entity.position.distance(Camp.position) <= entity.radius:
                    if self.itemTarget.itemType == ItemType.Wood:
                        Camp.woodCount += 1

                    elif self.itemTarget.itemType == ItemType.IronIngot:
                        Camp.ironIngotCount += 1

                    elif self.itemTarget.itemType == ItemType.IronOre:
                        Camp.ironOreCount += 1

                    Camp.itemsContainer.remove(self.itemTarget)

                    self.itemTarget = None
            else:
                entity.moveTo(self.itemTarget.position)
                if entity.position.distance(self.itemTarget.position) <= 16:
                    self.itemTarget.isPickedUp = True

        elif self.treeTarget:

            # busy chopping down tree
            if self.isChoppingTree:
                # update tree timer
                self.treeTarget.update()

                # if chopped, remove tree and swap into wood
                if self.treeTarget.isChopped and self.treeTarget in Camp.treesContainer:
                    Camp.treesContainer.remove(self.treeTarget)

                    node = SETTINGS.getNode(self.treeTarget.position, False)
                    if node:
                        node.images.pop(0)

                    item = Item(self.treeTarget.position, ItemType.Wood)
                    Camp.itemsContainer.append(item)

                    self.treeTarget = None
                    self.isChoppingTree = False
            else:
                # start tree timer if close, else move towards the tree
                distanceToTree = self.treeTarget.position.distance(entity.position)
                if distanceToTree <= entity.radius:
                    self.isChoppingTree = True
                    self.treeTarget.startTimer()
                else:

                    t = threading.Thread(target=entity.moveTo, args=(self.treeTarget.position,))
                    t.start()

        else:
            # locate items
            closestDistance = 0
            selectedItem = None
            # search the surrounding area for nearby items to pick up
            for item in Camp.itemsContainer:
                if item and not item.isTarget and not item.isPickedUp:

                    distanceToSub = item.position.distance(entity.position)

                    if closestDistance == 0 or distanceToSub < closestDistance:
                        closestDistance = distanceToSub
                        item.isTarget = True
                        item.isPickedUp = True
                        selectedItem = item

            if selectedItem:
                self.itemTarget = selectedItem

            # find a tree to chop
            if not self.itemTarget:
                distToTree = 0
                for tree in Camp.treesContainer:
                    #if tree.isChopped or tree.isTarget:
                        #continue

                    treeNode = SETTINGS.getNode(tree.position)
                    if not treeNode or not treeNode.isVisible:
                        continue

                    distTreeToEnt = tree.position.distance(entity.position)

                    if distTreeToEnt < distToTree or distToTree == 0:
                        tree.isTarget = True
                        self.treeTarget = tree

    def exit(self, entity):
        pass
