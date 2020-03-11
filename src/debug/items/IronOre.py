from debug.items.IPickupItem import IPickupItem


class IronOre(IPickupItem):
    def __init__(self, spawnPoint):
        super().__init__()
        self.position = spawnPoint

    def update(self):
        pass