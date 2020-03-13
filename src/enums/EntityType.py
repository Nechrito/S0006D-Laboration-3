from enum import Enum, auto


class EntityType(Enum):
    Worker   = auto()
    Explorer = auto()
    Builder  = auto()
    Artisan  = auto() # <- todo: 4 character traits for Artisans


