import time


class Tree:
    def __init__(self, spawnPoint):
        self.position = spawnPoint
        self.duration = 1  # the time it takes to cut down the tree
        self.timerStart = None
        self.isChopped = False
        self.isTarget = False

    def startTimer(self):
        self.timerStart = time.time()

    def update(self):
        if not self.timerStart or self.isChopped:
            return

        if time.time() - self.timerStart > self.duration:
            self.isChopped = True