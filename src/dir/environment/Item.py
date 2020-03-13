from dir.math.Vector import vec2
from enums.ItemType import ItemType


class Item:
    position: vec2

    def __init__(self, spawnPoint, itemType: ItemType):
        self.position = spawnPoint
        self.itemType = itemType

        self.isPickedUp = False
        self.isTarget = False # If an entity is approaching, to prevent multiple entities on the same object
