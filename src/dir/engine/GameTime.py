from datetime import datetime
import time

import pygame
import datetime


class GameTime:

    timeScale = 1
    ticks = 0

    lastFrame = 0
    deltaTime = 0
    fixedDeltaTime = 0

    gameDate: datetime
    cachedTime: time

    @classmethod
    def init(cls):
        cls.gameDate = datetime.datetime.now()
        cls.ticks = pygame.time.get_ticks()
        cls.cachedTime = cls.ticks

    @classmethod
    def setScale(cls, scale):
        cls.timeScale = scale
        return cls.timeScale

    @classmethod
    def updateTicks(cls):

        cls.ticks = pygame.time.get_ticks()

        cls.deltaTime = cls.fixedDeltaTime = ((cls.ticks - cls.lastFrame) / 1000)
        cls.deltaTime *= cls.timeScale  # post multiplying only here prevents fixedDeltaTime from scaling

        cls.lastFrame = cls.ticks

        elapsed = (cls.ticks - cls.cachedTime) * cls.timeScale
        if elapsed >= cls.relativeDuration(1):  # for each second in the game, add 1 minute to the game-time
            cls.gameDate = (cls.gameDate + datetime.timedelta(minutes=1))
            cls.cachedTime = cls.ticks

    @classmethod
    def timeElapsed(cls):
        return cls.gameDate.strftime("%d/%m-%y %H:%M")

    @classmethod
    def minutesToMilliseconds(cls, minute):
        return (minute * 60000) / cls.timeScale

    @classmethod
    def relativeDuration(cls, seconds):
        return seconds / cls.timeScale

    @classmethod
    def timeSince(cls, ticksStart):
        return (cls.ticks - ticksStart) * cls.timeScale