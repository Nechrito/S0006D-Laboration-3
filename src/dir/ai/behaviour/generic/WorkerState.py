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
        Message.sendConsole(entity, "Sure could make use of more wood 'n' ores")

    def handleMessage(self, telegram):
        pass

    def execute(self, entity):

        # update selected item
        if self.selectedItem:
            self.updateItem(entity)

        # update selected tree
        elif self.selectedTree:
            self.updateTree(entity)
        # locate tree, then item if no tree found
        else:
            item = self.findItem(entity)
            if item:
                self.selectedItem = item
            else:
                tree = self.findTree(entity)
                if tree:
                    self.selectedTree = tree

    def updateItem(self, entity):
        # move to camp once the item is picked up
        if self.selectedItem.isPickedUp:
            entity.moveTo(Camp.position)

            self.selectedItem.position = entity.position

            if entity.position.distance(Camp.position) <= entity.radius:

                if self.selectedItem.itemType == ItemType.Wood:
                    Camp.woodCount += 1
                elif self.selectedItem.itemType == ItemType.Charcoal:
                    Camp.charcoalCount += 1
                elif self.selectedItem.itemType == ItemType.Ingot:
                    Camp.ironIngotCount += 1
                elif self.selectedItem.itemType == ItemType.Ore:
                    Camp.ironOreCount += 1
                elif self.selectedItem.itemType == ItemType.Sword:
                    Camp.swordCount += 1

                if self.selectedItem:
                    if self.selectedItem in Camp.items:
                        Camp.items.remove(self.selectedItem)

                    self.selectedItem = None

        # move towards the item to then pick it up
        else:
            entity.moveTo(self.selectedItem.position)
            if entity.position.distance(self.selectedItem.position) <= entity.radius:
                self.selectedItem.isPickedUp = True

    def updateTree(self, entity):
        # busy chopping down tree
        if self.isChoppingTree:
            # update tree timer
            self.selectedTree.update(entity)

            # if chopped, remove tree and swap into wood
            if self.selectedTree.isChopped and self.selectedTree in Camp.trees:
                Camp.trees.remove(self.selectedTree)

                self.selectedItem = Item(self.selectedTree.position.randomized(15, 6, 0), ItemType.Wood)
                Camp.items.append(self.selectedItem)

                self.selectedTree = None
                self.isChoppingTree = False
        else:
            # start tree timer if close, else move towards the tree
            if self.selectedTree.position.distance(entity.position) <= entity.radius:
                self.isChoppingTree = True
                self.selectedTree.startTimer()
            else:
                entity.moveTo(self.selectedTree.position)

    def findTree(self, entity):
        # find a tree to chop
        distToEntCached = 0
        selectedTree = None
        for tree in Camp.trees:
            if tree.isTarget:
                continue

            treeNode = SETTINGS.getNode(tree.position, False, False)
            if not treeNode or not treeNode.isVisible:
                continue

            distTreeToEnt = tree.position.distance(Camp.position)

            if distTreeToEnt < distToEntCached or not selectedTree:
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
        for item in Camp.items:
            if not item.isTarget and not item.isPickedUp:

                itemNode = SETTINGS.getNode(item.position, False, False)
                if not itemNode or not itemNode.isVisible:
                    continue

                distanceToSub = item.position.distance(entity.position)

                if not selectedItem or distanceToSub < closestDistance:
                    closestDistance = distanceToSub
                    selectedItem = item

        if selectedItem:
            selectedItem.isTarget = True
            return selectedItem
        return None

    def exit(self, entity):
        pass
