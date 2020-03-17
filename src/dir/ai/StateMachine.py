class StateMachine:

    def __init__(self, entity, startState, globalState):
        self.owner = entity
        self.globalState = globalState
        self.locked = False
        self.previousState = None
        self.currentState = startState
        self.currentState.enter(self.owner)

    def update(self):
        self.currentState.execute(self.owner)
        self.globalState.execute(self.owner)

    def handleMessage(self, telegram):
        self.currentState.handleMessage(telegram)
        self.globalState.handleMessage(telegram)

    def setLockedState(self, value):
        self.locked = value

    def revert(self):
        if self.previousState is not None:
            self.change(self.previousState)

    def change(self, nextState):

        if self.locked:
            return

        self.previousState = self.currentState

        self.currentState.exit(self.owner)

        self.currentState = nextState

        self.currentState.enter(self.owner)
