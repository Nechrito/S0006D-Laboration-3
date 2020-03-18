from enum import Enum, auto


class MessageType(Enum):
    PositionChange = auto() # assumes message is a vec2
    StateChange = auto() # assumes message is a new EntityState
    RevertState = auto()
    CraftRequest = auto() # assumes message is a BuildingType or ItemType
    LevelUp = auto() # when camp has leveled up, another solution would be a callback function

