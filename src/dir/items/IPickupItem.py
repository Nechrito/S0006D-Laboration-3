import abc

from dir.math.Vector import vec2


class IPickupItem(object, metaclass=abc.ABCMeta):
    position: vec2

    def __init__(self, spawnPoint):
        self.position = spawnPoint
        self.isValid = True
        self.isPickedUp = False
        self.isTarget = False # If an entity is approaching, to prevent multiple entities on the same object

    #@abc.abstractmethod
    def TogglePickup(self):
        self.isPickedUp = not self.isPickedUp