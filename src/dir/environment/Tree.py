import time


class Tree:
    def __init__(self, spawnPoint):
        self.position = spawnPoint
        self.duration = 0.5
        self.timerStart = 0
        self.isChopped = False
        self.isTarget = False

    def startTimer(self):
        self.timerStart = time.time()

    def update(self):
        if time.time() - self.timerStart > self.duration:
            self.isChopped = True