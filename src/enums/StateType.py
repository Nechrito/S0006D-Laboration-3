from enum import Enum, auto


class StateType(Enum):
    IdleState = auto()
    WorkState = auto()
    ExploreState = auto()
    ArtisanMiner = auto()
    ArtisanCraftsman = auto()
    ArtisanSmelter = auto()
    ArtisanSmith = auto()


