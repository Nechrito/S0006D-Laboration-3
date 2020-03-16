import time

from dir.ai.StateTransition import StateTransition
from dir.ai.behaviour.IState import IState
from dir.environment.Camp import GameTime, Camp
from enums.StateType import StateType

from enums.EntityType import EntityType


class IdleState(IState):
    def __init__(self):
        pass

    def enter(self, entity):
        pass

    def execute(self, entity):

        if entity.entityType == EntityType.Worker:
            StateTransition.setState(entity, StateType.WorkState)

        elif entity.entityType == EntityType.Explorer:
            # a bit hacky, but essentially when an agent is done exploring
            # the agent will go back into idle and wait for the Camp to level up
            if time.time() - Camp.lastLevelUpTick <= 1000:
                StateTransition.setState(entity, StateType.ExploreState)

        elif entity.entityType == EntityType.Miner:
            StateTransition.setState(entity, StateType.ArtisanMiner)

        elif entity.entityType == EntityType.Craftsman:
            StateTransition.setState(entity, StateType.ArtisanCraftsman)

        elif entity.entityType == EntityType.Smelter:
            StateTransition.setState(entity, StateType.ArtisanSmelter)

        elif entity.entityType == EntityType.Smith:
            StateTransition.setState(entity, StateType.ArtisanSmith)

    def exit(self, entity):
        pass
