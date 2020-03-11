import abc

from debug.math.Vector import vec2


class IPickupItem(object, metaclass=abc.ABCMeta):
    position: vec2

    def __init__(self, spawnPoint):
        self.position = spawnPoint
        self.isValid = True
        self.isPickedUp = False

    #@abc.abstractmethod
    def TogglePickup(self):
        self.isPickedUp = not self.isPickedUp