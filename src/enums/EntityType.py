from enum import Enum, auto


class EntityType(Enum):
    Worker   = auto()
    Explorer = auto()
    ArtisanMiner = auto()
    ArtisanSmith = auto
    ArtisanSmelt = auto
    ArtisanCraftsman = auto()
