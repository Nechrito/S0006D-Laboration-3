from dir.ai.StateTransition import StateTransition
from dir.ai.behaviour.IState import IState
from enums.EntityType import EntityType
from enums.MessageType import MessageType
from enums.StateType import StateType
from src.dir.ai.Entity import Entity


class GlobalState(IState):

    def __init__(self):
        self.entity = None

    def enter(self, entity: Entity):
        self.entity = entity

    def handleMessage(self, telegram):
        if not self.entity:
            if telegram.target:
                self.entity = telegram.target
            else:
                return
        print("1")
        if telegram.messageType == MessageType.RevertState:
            self.entity.revertState()
        elif telegram.messageType == MessageType.StateChange:

            if self.entity.entityType == EntityType.Worker:
                StateTransition.setState(self.entity, StateType.WorkState)

            elif self.entity.entityType == EntityType.Explorer:
                StateTransition.setState(self.entity, StateType.ExploreState)

            elif self.entity.entityType == EntityType.Miner:
                StateTransition.setState(self.entity, StateType.ArtisanMiner)

            elif self.entity.entityType == EntityType.Craftsman:
                StateTransition.setState(self.entity, StateType.ArtisanCraftsman)

            elif self.entity.entityType == EntityType.Smelter:
                StateTransition.setState(self.entity, StateType.ArtisanSmelter)

            elif self.entity.entityType == EntityType.Smith:
                StateTransition.setState(self.entity, StateType.ArtisanSmith)

    def execute(self, entity: Entity):
        pass

    def exit(self, entity: Entity):
        pass
