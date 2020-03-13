import time

from dir.engine.GameTime import GameTime


class Tree:
    def __init__(self, spawnPoint):
        self.position = spawnPoint
        self.duration = 1  # the time it takes to cut down the tree
        self.timerStart = None
        self.isChopped = False
        self.isTarget = False

    def startTimer(self):
        self.timerStart = time.time()
        print("Timer started")

    def update(self):
        if time.time() - self.timerStart > self.duration:
            self.isChopped = True