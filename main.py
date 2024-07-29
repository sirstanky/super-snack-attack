import pygame as pg

import constants as c
from controls.game import MainGame
from controls.mainmenu import MainMenu
from controls.pausemenu import PauseMenu

# Initialize pygame
pg.init()

# Set up the game window
c.window = pg.display.set_mode((c.window_width, c.window_height))
pg.display.set_caption("Super Snack Attack!")

# Set up game variables
c.clock = pg.time.Clock()

game = MainGame()
# TODO Set up call to create main game
menu = MainMenu()
pause = PauseMenu()

running = True
command = menu.running()
while running:
    if command == 'play':
        command = game.play()
    if command == 'paused':
        command = pause.start()
    if command == 'quit':
        running = False


print("Quit with elegance")
pg.quit()
