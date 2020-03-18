from enums.StateType import StateType


class StateTransition:

    @classmethod
    def revertState(cls, entity):
        entity.revertState()

    @classmethod
    def setState(cls, entity, stateType):
        if stateType == StateType.IdleState:
            from dir.ai.behaviour.generic.IdleState import IdleState
            entity.setState(IdleState())

        elif stateType == StateType.WorkState:
            from dir.ai.behaviour.generic.WorkerState import WorkerState
            entity.setState(WorkerState())

        elif stateType == StateType.ExploreState:
            from dir.ai.behaviour.generic.ExploreState import ExploreState
            entity.setState(ExploreState())

        elif stateType == StateType.ArtisanCraftsman:
            from dir.ai.behaviour.artisan.CraftState import CraftState
            entity.setState(CraftState())

        elif stateType == StateType.ArtisanMiner:
            from dir.ai.behaviour.artisan.MineState import MineState
            entity.setState(MineState())

        elif stateType == StateType.ArtisanSmelter:
            from dir.ai.behaviour.artisan.SmeltState import SmeltState
            entity.setState(SmeltState())

        elif stateType == StateType.ArtisanSmith:
            from dir.ai.behaviour.artisan.SmithState import SmithState
            entity.setState(SmithState())

    @classmethod
    def create_instance(cls, class_name, instance_name):
        count = 0
        while True:
            name = instance_name + str(count)
            globals()[name] = class_name()
            count += 1
            print('Class instance: {}'.format(name))
            yield True