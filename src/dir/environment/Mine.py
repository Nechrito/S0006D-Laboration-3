import time


class Mine:
    # produces charcoal, requires 1 craftsman + 10 trees + 60s to produce 1 mine
    def __init__(self, spawnPoint):
        self.position = spawnPoint
        self.owner = None
        self.duration = 20
        self.timerStart = 0
        self.isProduced = False

    def startProducing(self):
        if self.timerStart == 0:
            self.timerStart = time.time()

    def update(self):
        if self.timerStart == 0 or self.isProduced:
            return

        if time.time() - self.timerStart > self.duration:
            self.isProduced = True
            self.timerStart = 0