from dir.environment.Camp import Camp
from enums.BuildingType import BuildingType
from enums.EntityType import EntityType
from enums.ItemType import ItemType

from dir.ai.behaviour.IState import IState
from dir.ai.Message import Message


class MineState(IState):
    def __init__(self):
        self.selected = None
        self.selectedPos = None # to allow going towards a randomized position
        self.reached = False

    def enter(self, entity):
        Message.sendConsole(entity, "Headin' over to the mines")

    def handleMessage(self, telegram):
        pass

    def execute(self, entity):
        if not self.selected:
            for building in Camp.buildings:
                if building.buildingType != BuildingType.Mine:
                    continue

                if not building.owner:
                    building.owner = entity
                    self.selected = building
                    self.selectedPos = self.selected.position.randomized(10, 4, 2)
                    break

        if not self.selected:
            return

        if self.reached:
            if self.selected.isCrafted:
                self.selected.startProducing(ItemType.Charcoal)
                self.selected.updateItemTimer(entity)

        elif entity.position.distance(self.selectedPos) <= entity.radius:
            self.reached = True # <- lessens the amount of .distance(...) calls
        elif self.selected:
            entity.moveTo(self.selectedPos)

    def exit(self, entity):
        pass
