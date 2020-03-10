import time


class Tree:
    def __init__(self, spawnPoint):
        self.position = spawnPoint
        self.duration = 30  # the time to cut down the tree
        self.timerStart = None
        self.isAlive = True

    def startTimer(self):
        self.timerStart = time.time()

    def update(self):
        if time.time() - self.timerStart > self.duration:
            self.isAlive = False