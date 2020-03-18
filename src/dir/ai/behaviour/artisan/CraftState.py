from dir.environment.Building import Building
from dir.environment.Camp import Camp
from enums.BuildingType import BuildingType
from enums.EntityType import EntityType
from dir.ai.behaviour.IState import IState
from dir.ai.Message import Message
from enums.MessageType import MessageType


class CraftState(IState):
    selected: Building

    def __init__(self):
        self.selected = None
        self.locked = True # if we get a msg that we should craft something, wait until we can craft it

    def enter(self, entity):
        entity.setType(EntityType.Craftsman)
        Message.sendConsole(entity, "What to build today..")

    def handleMessage(self, telegram):
        if telegram.messageType and telegram.messageType == MessageType.CraftRequest:
            dist = Camp.radius // 16
            self.selected = Building(Camp.position.randomized(iterations=10, maxDist=dist * 0.75, minDist=dist * 0.20), telegram.message)
            self.locked = True

    def execute(self, entity):
        if self.selected:

            # update the production timer
            if not self.selected.isCrafted:

                if self.selected.timerStart == 0 and Camp.canProduce(self.selected.buildingType):
                    Message.sendConsole(entity, "Buildin' a brand new " + self.selected.name)
                    self.selected.startBuilding()

                self.selected.update()
            else:
                self.selected = None
        elif not self.locked: # most of the underlying code here wont be used, as it's now based on messaging

            # amount of each building type created
            mines = 0
            smiths = 0
            smelts = 0
            trainings = 0
            comp = []

            for building in Camp.buildings:
                if building.buildingType == BuildingType.Mine:
                    mines += 1
                elif building.buildingType == BuildingType.Smith:
                    smiths += 1
                elif building.buildingType == BuildingType.Smelt:
                    smelts += 1
                elif building.buildingType == BuildingType.TrainingCamp:
                    trainings += 1

            # the min value of list may be used to help select what to craft next
            comp.append(mines)
            comp.append(smiths)
            comp.append(smelts)
            comp.append(trainings)

            fewest = min(comp)
            buildingType = None

            # add whichever building we can, based on a priority (which comes of the enum index)
            # todo: would be a good idea here to send a msg to workers that they need to fetch certain materials
            if fewest == mines and Camp.canProduce(BuildingType.Mine):
                buildingType = BuildingType.Mine
            elif fewest == smiths and Camp.canProduce(BuildingType.Smith):
                buildingType = BuildingType.Smith
            elif fewest == smelts and Camp.canProduce(BuildingType.Smelt):
                buildingType = BuildingType.Smelt
            elif fewest == trainings and Camp.canProduce(BuildingType.TrainingCamp):
                buildingType = BuildingType.TrainingCamp

            # if no building can be produced, exit
            if not buildingType:
                return

            # create a new building at camp, todo: code requires a cleanup in future
            dist = Camp.radius // 16
            building = Building(Camp.position.randomized(iterations=10, maxDist=dist * 0.75, minDist=dist * 0.20), buildingType)
            if building.position:
                self.selected = building
                self.selected.startBuilding()

    def exit(self, entity):
        pass
