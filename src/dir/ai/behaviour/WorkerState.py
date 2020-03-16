import threading

from dir.environment.Camp import Camp
from dir.environment.Item import Item
from enums.ItemType import ItemType

from src.dir.ai.Entity import SETTINGS
from dir.ai.behaviour.IState import IState
from dir.ai.Message import Message


class WorkerState(IState):
    def __init__(self):
        self.isChoppingTree = False
        self.selectedTree = None
        self.selectedItem = None
        self.searchRadius = 16 * 4

    def enter(self, entity):
        Message.sendConsole(entity, "Sure could make use of more wood, will fetch some")

    def execute(self, entity):

        # update selected tree
        if self.selectedTree:
            self.updateTree(entity)

        # update selected item
        elif self.selectedItem:
            self.updateItem(entity)

        # locate tree, then item if no tree found
        else:

            tree = self.findTree(entity)
            if tree:
                self.selectedTree = tree
            else:
                item = self.findItem(entity)
                if item:
                    self.selectedItem = item

    def updateItem(self, entity):
        # move to camp once the item is picked up
        if self.selectedItem.isPickedUp:
            t = threading.Thread(target=entity.moveTo, args=(Camp.position,))
            t.start()
            t.join()
            self.selectedItem.position = entity.position

            if entity.position.distance(Camp.position) <= entity.radius:
                if self.selectedItem.itemType == ItemType.Wood:
                    Camp.woodCount += 1
                elif self.selectedItem.itemType == ItemType.Ingot:
                    Camp.ironIngotCount += 1
                elif self.selectedItem.itemType == ItemType.Ore:
                    Camp.ironOreCount += 1

                Camp.itemsContainer.remove(self.selectedItem)
                self.selectedItem = None

        # move towards the item to then pick it up
        else:
            t = threading.Thread(target=entity.moveTo, args=(self.selectedItem.position,))
            t.start()
            t.join()

            if entity.position.distance(self.selectedItem.position) <= entity.radius:
                self.selectedItem.isPickedUp = True

    def updateTree(self, entity):
        # busy chopping down tree
        if self.isChoppingTree:
            # update tree timer
            self.selectedTree.update()

            # if chopped, remove tree and swap into wood
            if self.selectedTree in Camp.treesContainer:
                Camp.treesContainer.remove(self.selectedTree)

                node = SETTINGS.getNode(self.selectedTree.position, False)
                if node:
                    node.images.pop(0)

                self.selectedItem = Item(self.selectedTree.position, ItemType.Wood)
                self.selectedItem.isPickedUp = True
                Camp.itemsContainer.append(self.selectedItem)

                self.selectedTree = None
                self.isChoppingTree = False
        else:
            # start tree timer if close, else move towards the tree
            distanceToTree = self.selectedTree.position.distance(entity.position)
            if distanceToTree <= entity.radius:
                self.selectedTree.startTimer()
                self.isChoppingTree = True
            else:

                t = threading.Thread(target=entity.moveTo, args=(self.selectedTree.position,))
                t.start()
                t.join()

    def findTree(self, entity):
        # find a tree to chop
        distToEntCached = 0
        selectedTree = None
        for tree in Camp.treesContainer:
            if tree.isTarget:
                continue

            treeNode = SETTINGS.getNode(tree.position)
            if not treeNode or not treeNode.isVisible:
                continue

            distTreeToEnt = tree.position.distance(Camp.position)
            if distTreeToEnt < distToEntCached or not self.selectedTree:
                distToEntCached = distTreeToEnt
                selectedTree = tree

        if selectedTree:
            selectedTree.isTarget = True
            return selectedTree
        return None

    def findItem(self, entity):
        # locate items
        closestDistance = 0
        selectedItem = None
        # search the surrounding area for nearby items to pick up
        for item in Camp.itemsContainer:
            if not item.isTarget and not item.isPickedUp:
                distanceToSub = item.position.distance(entity.position)

                if not selectedItem or distanceToSub < closestDistance:
                    closestDistance = distanceToSub
                    selectedItem = item

        if selectedItem:
            selectedItem.isTarget = True
            selectedItem.isPickedUp = True
            return selectedItem
        return None

    def exit(self, entity):
        pass
