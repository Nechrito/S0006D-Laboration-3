import time
import pygame


class Tree:
    def __init__(self, spawnPoint, image):
        self.position = spawnPoint
        self.image = pygame.transform.scale(image, (32, 48))
        self.rect = self.image.get_rect()
        self.rect.center = (self.position.X + 8, self.position.Y + 8)

        self.duration = 0.5
        self.timerStart = 0
        self.isTarget = False

    def startTimer(self):
        self.timerStart = time.time()

    def update(self):
        if time.time() - self.timerStart > self.duration:
            self.isChopped = True