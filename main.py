import sys
from os import path

import pygame
import pygame.freetype

from dir.engine.EntityManager import EntityManager
from dir.engine.TaskManager import TaskManager
from src.Game import Game
from src.dir.engine.GameTime import GameTime
from src.dir.engine.UserInput import UserInput

# Only executes the main method if this module is executed as the main script
if __name__ == "__main__":

    folder = "resources/"
    if getattr(sys, 'frozen', False):
        directory = path.dirname(sys.executable)
    else:
        directory = path.dirname(__file__)

    pygame.init()
    pygame.mixer.init()
    pygame.freetype.init()

    GameTime.init()
    TaskManager.init()
    EntityManager.init()

    instance = Game(directory, folder)
    userInput = UserInput(instance)

    while True:
        # Lessen CPU usage of the app
        if not pygame.key.get_focused():
            pygame.time.wait(10)

        # Core
        GameTime.updateTicks()
        userInput.update()
        instance.update()
        instance.draw()
