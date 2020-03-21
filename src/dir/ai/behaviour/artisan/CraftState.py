from dir.environment.Building import Building
from dir.environment.Camp import Camp
from enums.BuildingType import BuildingType
from dir.ai.behaviour.IState import IState
from dir.ai.Message import Message
from enums.MessageType import MessageType


class CraftState(IState):
    selected: Building

    def __init__(self):
        self.selected = None
        self.locked = True # if we get a msg that we should craft something, wait until we can craft it

    def enter(self, entity):
        Message.sendConsole(entity, "What to build today..")

    def handleMessage(self, telegram):
        if telegram.messageType and telegram.messageType == MessageType.CraftRequest:
            self.selected = Building(Camp.position.randomized(iterations=10, maxDist=11, minDist=6), telegram.message)
            self.locked = True

    def execute(self, entity):

        if self.selected:
            # update the production timer
            if not self.selected.isCrafted:
                self.selected.updateBuildingTimer(entity)
            elif not self.selected.isCrafting and Camp.canProduce(self.selected.buildingType):
                Message.sendConsole(entity, "Buildin' a brand new " + self.selected.name)
                self.selected.startBuilding()
                # self.locked = False
            else:
                self.selected = None

    def exit(self, entity):
        pass
