from dir.environment.Camp import Camp
from enums.BuildingType import BuildingType
from enums.EntityType import EntityType
from enums.ItemType import ItemType

from dir.ai.behaviour.IState import IState
from dir.ai.Message import Message


class SmithState(IState):
    def __init__(self):
        self.selected = None
        self.reached = False

    def enter(self, entity):
        entity.setType(EntityType.Smith)
        Message.sendConsole(entity, "I wonder how many swords I can produce today")

    def execute(self, entity):
        if not self.selected:
            for building in Camp.buildings:
                if building.buildingType != BuildingType.Smith:
                    continue

                if not building.owner:
                    building.owner = entity
                    self.selected = building
                    break

        if not self.selected:
            return

        if self.reached:
            if self.selected.isCrafted:
                self.selected.startProducing(ItemType.Sword)
                self.selected.update()
            else:
                self.selected.startBuilding()

        elif self.selected and entity.position.distance(self.selected.position) <= entity.radius:
            self.reached = True
        elif self.selected:
            entity.moveTo(self.selected.position)

    def exit(self, entity):
        pass
