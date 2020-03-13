from enum import Enum, auto


class EntityType(Enum):
    Worker   = auto()
    Explorer = auto()
    Builder  = auto()
    ArtisanMiner = auto() # <- todo: 4 character traits for Artisans
    ArtisanSmith = auto
    ArtisanSmelt = auto
    ArtisanCraftsman = auto()
