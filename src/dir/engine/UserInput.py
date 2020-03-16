import sys

import pygame

from src.dir.engine.GameTime import GameTime


class UserInput:
    def __init__(self, game):
        self.instance = game
        self.timeScaleCurrent = GameTime.timeScale

    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.instance.onClick()
            if event.type == pygame.KEYDOWN:
                # Exit
                if event.type == pygame.QUIT or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Toggle mouse
                if event.key == pygame.K_LALT:
                    self.instance.realCursorEnabled = not self.instance.realCursorEnabled
                    pygame.mouse.set_visible(self.instance.realCursorEnabled)
                    pygame.event.set_grab(not self.instance.realCursorEnabled)




                # Pause game
                if event.key == pygame.K_SPACE:
                    if self.instance.paused:
                        GameTime.setScale(self.timeScaleCurrent)
                    else:
                        GameTime.setScale(0.00001)

                    self.instance.paused = not self.instance.paused

                # Speed up
                if not self.instance.paused and event.key == pygame.K_LSHIFT:
                    self.timeScaleCurrent = GameTime.setScale(self.timeScaleCurrent * 2)
                # Slow down
                if not self.instance.paused and event.key == pygame.K_LCTRL:
                    self.timeScaleCurrent = GameTime.setScale(self.timeScaleCurrent / 2)

