import time


class Smith:
    # produces swords, requires 1 craftsman + 10 trees + 120s to produce 1 smith
    def __init__(self, spawnPoint):
        self.position = spawnPoint
        self.duration = 40
        self.timerStart = 0
        self.producedCount = 0

    def startProducing(self):
        if self.timerStart == 0:
            self.timerStart = time.time()

    def update(self):
        if self.timerStart == 0:
            return

        if time.time() - self.timerStart > self.duration:
            self.producedCount += 1
            self.timerStart = 0