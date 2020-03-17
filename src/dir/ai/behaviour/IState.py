import abc


class IState(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def enter(self, entity):
        pass

    @abc.abstractmethod
    def handleMessage(self, telegram):
        pass

    @abc.abstractmethod
    def execute(self, entity):
        pass

    @abc.abstractmethod
    def exit(self, entity):
        pass


