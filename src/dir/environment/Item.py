import time

from dir.math.Vector import vec2
from enums.ItemType import ItemType


class Item:
    position: vec2

    def __init__(self, spawnPoint: vec2, itemType: ItemType):
        self.position = spawnPoint
        self.itemType = itemType
        self.name = str(self.itemType).replace("ItemType.", "")

        if itemType == ItemType.Charcoal:
            self.duration = 30
        elif itemType == ItemType.Ingot:
            self.duration = 30 # is not assigned to any specific number according to the assignment
        if itemType == ItemType.Sword:
            self.duration = 60

        self.isProducing = False
        self.isPickedUp = False
        self.isTarget = False # If an entity is approaching, to prevent multiple entities on the same object

    def startProducing(self):
        self.isProducing = True
        self.timerStart = time.time()
       # print("Creating: " + self.name)

    def update(self):
        if not self.isProducing:
            return

        if self.timerStart != 0 and time.time() - self.timerStart > self.duration:
            self.isProducing = False
           # print("Created: " + self.name)
