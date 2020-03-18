from enums.EntityType import EntityType
from enums.MessageType import MessageType


class Telegram:

    def __init__(self, message=None, source = None, entityType: EntityType = None, messageType: MessageType = None, target = None):
        self.message = message
        self.source = source
        self.entityType = entityType
        self.messageType = messageType
        self.target = target

    def isForMe(self, entity):
        return (self.target and self.target == entity) or (self.entityType and self.entityType == entity.entityType)

    def isMyType(self, entity):
        return self.entityType and self.entityType == entity.entityType