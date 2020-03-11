from dir.ai.behaviour.IState import IState
from enums.EntityType import EntityType


class IdleState(IState):
    def __init__(self):
        pass

    def enter(self, entity):
        pass

    def execute(self, entity):

        if entity.characterType == EntityType.Worker:
            from .TreeState import TreeState as state
            entity.setState(state())

        elif entity.characterType == EntityType.Explorer:
            from .ExploreState import ExploreState
            entity.setState(ExploreState())

        elif entity.characterType == EntityType.Builder:
            from .BuildingState import BuildingState as state
            entity.setState(state())

        elif entity.characterType == EntityType.Soldier:
            from .TreeState import TreeState as state
            entity.setState(state())

    def exit(self, entity):
        pass
