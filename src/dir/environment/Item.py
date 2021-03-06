import time

from dir.math.Vector import vec2
from enums.ItemType import ItemType


class Item:
    position: vec2

    def __init__(self, spawnPoint: vec2, itemType: ItemType):
        self.position = spawnPoint
        self.itemType = itemType
        self.name = str(self.itemType).replace("ItemType.", "")
        self.color = (255, 255, 255) # for text rendering
        self.duration = 1

        if itemType == ItemType.Charcoal:
            self.color = (51, 51, 51)
            self.duration = 30
        elif itemType == ItemType.Ingot:
            self.color = (158, 158, 157)
            self.duration = 30 # is not assigned to any specific number according to the assignment
        elif itemType == ItemType.Sword:
            self.color = (252, 252, 83)
            self.duration = 60
        elif itemType == ItemType.Ore:
            self.color = (128, 122, 115)
        elif itemType == ItemType.Wood:
            self.color = (196, 171, 134)

        self.isProducing = False
        self.isProduced = False
        self.isPickedUp = False
        self.isTarget = False # If an entity is approaching, to prevent multiple entities on the same object

    def startProducing(self):
        self.isProducing = True
        self.timerStart = time.time()

    def update(self, entity):
        if not self.isProducing:
            return

        if time.time() - self.timerStart >= self.duration / entity.scaleTime:
            self.isProducing = False
            self.isProduced = True
