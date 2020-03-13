from enum import Enum, auto


class StateType(Enum):
    IdleState = auto()
    WorkState = auto()
    ExploreState = auto()
    BuildState = auto()
    ArtisanMiner = auto()
    ArtisanCraftsman = auto()
    ArtisanSmelter = auto()
    ArtisanSmith = auto()


