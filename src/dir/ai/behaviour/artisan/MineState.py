from dir.environment.Camp import Camp
from dir.environment.Item import Item
from enums.BuildingType import BuildingType
from enums.EntityType import EntityType
from enums.ItemType import ItemType

from dir.ai.behaviour.IState import IState
from dir.ai.Message import Message


class MineState(IState):
    def __init__(self):
        self.selected = None
        self.reached = False

    def enter(self, entity):
        entity.setType(EntityType.Miner)
        Message.sendConsole(entity, "Headin' over to the mines")

    def execute(self, entity):
        if not self.selected:
            for building in Camp.buildings:
                if building.buildingType != BuildingType.Mine:
                    continue

                if not building.owner:
                    building.owner = entity
                    self.selected = building
                    break

        if not self.selected:
            return

        if self.reached:
            if self.selected.isCrafted:
                self.selected.startProducing(ItemType.Charcoal)
                self.selected.update()
            else:
                self.selected.startBuilding()

        elif self.selected and entity.position.distance(self.selected.position) <= entity.radius:
            self.reached = True # <- lessens the amount of .distance(...) calls
        elif self.selected:
            entity.moveTo(self.selected.position)

    def exit(self, entity):
        pass
