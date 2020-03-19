import time

from dir.ai.Entity import Entity
from dir.engine.GameTime import GameTime
from dir.environment.Item import Item
from dir.math.Vector import vec2
from enums.BuildingType import BuildingType
from enums.ItemType import ItemType
from dir.environment.Camp import Camp


class Building:
    def __init__(self, position: vec2, buildingType: BuildingType, owner: Entity = None):
        self.position = position
        self.buildingType = buildingType
        self.name = str(self.buildingType).replace("BuildingType.", "")

        # int
        self.priority = self.buildingType.value
        self.item = None

        self.owner = owner
        self.duration = 0
        self.timerStart = 0
        self.isCrafted = False

        self.costWood = 0
        self.costIronOre = 0
        self.costIronIngot = 0
        self.costSword = 0

        # costs / duration
        if self.buildingType == BuildingType.Mine:
            self.costWood = 10
            self.duration = 60
        elif self.buildingType == BuildingType.Smith:
            self.costWood = 10
            self.costIronIngot = 3
            self.duration = 180
        elif self.buildingType == BuildingType.Smelt:
            self.costWood = 10
            self.duration = 120
        elif self.buildingType == BuildingType.TrainingCamp:
            self.costWood = 10
            self.duration = 120

    def startBuilding(self):
        if self.timerStart != 0:
            return

        Camp.woodCount  -= self.costWood
        Camp.swordCount -= self.costSword
        Camp.ironIngotCount -= self.costIronIngot
        Camp.ironOreCount   -= self.costIronOre
        self.timerStart = time.time()

    def startProducing(self, itemType: ItemType):
        if self.item:
            return

        self.item = Item(self.position.randomized(maxDist=3), itemType)
        self.item.startProducing()

    def update(self):

        # produce until finished
        if self.item:
            if self.item.isProducing:
                self.item.update()
            else:
                Camp.items.append(self.item)
                self.item = None

        # crafts the building itself
        if self.timerStart != 0 and not self.isCrafted: #  and time.time() - self.timerStart >= self.duration:
            self.isCrafted = True
            self.timerStart = 0
            Camp.buildings.append(self)

