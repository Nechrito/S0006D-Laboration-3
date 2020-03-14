from dir.environment.Camp import Camp
from dir.environment.Item import Item
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
        return
        if not self.selected:
            for mine in Camp.mines:
                if not mine.owner:
                    mine.owner = entity
                    self.selected = mine

        if not self.selected:
            return

        if self.reached:
            if self.selected.isProduced:
                Camp.itemsContainer.append(Item(self.selected.position, ItemType.Charcoal))
                self.selected.isProduced = False
            else:
                self.selected.update()
        elif entity.position.distance(self.selected) <= entity.radius:
            self.reached = True
        else:
            entity.moveTo(self.selected)

    def exit(self, entity):
        pass
