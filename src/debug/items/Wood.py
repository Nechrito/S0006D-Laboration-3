from debug.items.IPickupItem import IPickupItem


class Wood(IPickupItem):
    def __init__(self, spawnPoint):
        super().__init__(spawnPoint)
