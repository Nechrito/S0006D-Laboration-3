from dir.environment.Camp import Camp
from dir.environment.Item import Item
from enums.EntityType import EntityType
from enums.ItemType import ItemType

from dir.ai.behaviour.IState import IState
from dir.ai.Message import Message


class SmeltState(IState):
    def __init__(self):
        self.selected = None
        self.reached = False

    def enter(self, entity):
        entity.setType(EntityType.Smelter)
        Message.sendConsole(entity, "I wonder how many ingots I can produce today")

    def execute(self, entity):
        return
        if not self.selected:
            for complex in Camp.smeltingComplexes:
                if not complex.owner:
                    complex.owner = entity
                    self.selected = complex

        if not self.selected:
            return

        if self.reached:
            if self.selected.isProduced:
                Camp.itemsContainer.append(Item(self.selected.position, ItemType.Sword))
                self.selected.isProduced = False
            else:
                self.selected.update()
        elif entity.position.distance(self.selected) <= entity.radius:
            self.reached = True
        else:
            entity.moveTo(self.selected)

    def exit(self, entity):
        pass
