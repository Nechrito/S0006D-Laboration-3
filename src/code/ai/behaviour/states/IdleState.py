from code.ai.behaviour.states.IState import IState
from enums.EntityType import EntityType
from src.code.ai.messaging.Message import Message


class IdleState(IState):
    def __init__(self):
        pass

    def enter(self, entity):
        pass
        #Message.sendConsole(entity, "Nothing to do...")

    def execute(self, entity):

        if entity.characterType == EntityType.Worker:
            from .TreeState import TreeState as state
            entity.setState(state())

        elif entity.characterType == EntityType.Explorer:
            from .ExploreState import ExploreState as state
            entity.setState(state())

        elif entity.characterType == EntityType.Builder:
            from .BuildingState import BuildingState as state
            entity.setState(state())

        elif entity.characterType == EntityType.Soldier:
            from .TreeState import TreeState as state
            entity.setState(state())

    def exit(self, entity):
        pass
