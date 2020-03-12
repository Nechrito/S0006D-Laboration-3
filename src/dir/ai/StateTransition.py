from enums.StateType import StateType


class StateTransition:

    @classmethod
    def setState(cls, entity, stateType):
        if stateType == StateType.IdleState:
            from dir.ai.behaviour.IdleState import IdleState
            entity.setState(IdleState())

        elif stateType == StateType.WorkState:
            from dir.ai.behaviour.WorkerState import WorkerState
            entity.setState(WorkerState())

        elif stateType == StateType.ExploreState:
            from dir.ai.behaviour.ExploreState import ExploreState
            entity.setState(ExploreState())

        elif stateType == StateType.BuildState:
            from dir.ai.behaviour.BuildingState import BuildingState
            entity.setState(BuildingState())