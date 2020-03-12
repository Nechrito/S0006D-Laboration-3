from dir.ai.StateTransition import StateTransition
from dir.ai.behaviour.IState import IState
from dir.engine.Camp import Camp
from enums.StateType import StateType

from dir.engine.GameTime import GameTime
from enums.EntityType import EntityType


class IdleState(IState):
    def __init__(self):
        pass

    def enter(self, entity):
        pass

    def execute(self, entity):

        if entity.characterType == EntityType.Worker:
            StateTransition.setState(entity, StateType.WorkState)

        elif entity.characterType == EntityType.Explorer:
            # a bit hacky, but essentially when an agent is done exploring
            # the agent will go back into idle and wait for the Camp to level up
            if GameTime.ticks - Camp.lastLevelUpTick <= 1000:
                StateTransition.setState(entity, StateType.ExploreState)

        elif entity.characterType == EntityType.Builder:
            StateTransition.setState(entity, StateType.BuildState)


    def exit(self, entity):
        pass
