import abc

from src.code.ai.Entity import Entity


class IState(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def enter(self, entity: Entity):
        pass

    @abc.abstractmethod
    def execute(self, entity: Entity):
        pass

    @abc.abstractmethod
    def exit(self, entity: Entity):
        pass


