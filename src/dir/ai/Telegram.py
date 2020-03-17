from enums.EntityType import EntityType


class Telegram:

    def __init__(self, source, entityType: EntityType, messageType, msg):
        self.source = source
        self.entityType = entityType
        self.messageType = messageType
        self.message = msg