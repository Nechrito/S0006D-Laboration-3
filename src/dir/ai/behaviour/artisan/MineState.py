from dir.engine.Camp import Camp
from dir.environment.Item import Item
from enums.ItemType import ItemType

from dir.ai.behaviour.IState import IState
from dir.ai.Message import Message


class MineState(IState):
    def __init__(self):
        self.selectedMine = None
        self.reachedMine = False

    def enter(self, entity):
        Message.sendConsole(entity, "Headin' over to the mines")

    def execute(self, entity):
        if not self.selectedMine:
            for mine in Camp.mines:
                if not mine.owner:
                    mine.owner = entity
                    self.selectedMine = mine

        if not self.selectedMine:
            return

        if self.reachedMine:
            if self.selectedMine.isProduced:
                Camp.itemsContainer.append(Item(self.selectedMine.position, ItemType.Charcoal))
                self.selectedMine.isProduced = False
            else:
                self.selectedMine.update()
        elif entity.position.distance(self.selectedMine) <= entity.radius:
            self.reachedMine = True
        else:
            entity.moveTo(self.selectedMine)

    def exit(self, entity):
        pass
