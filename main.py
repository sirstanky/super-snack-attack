import pygame as pg

import constants as c

# Initialize pygame
pg.init()

# Set up the game window
c.window = pg.display.set_mode((c.window_width, c.window_height))
pg.display.set_caption("Super Snack Attack!")

# Set up game variables
c.clock = pg.time.Clock()

from controls.states.game import MainGame
from controls.states.mainmenu import MainMenu

c.game_state = [MainGame()]

while c.game_state:
    c.game_state[-1].run()

print("Quit with elegance")
pg.quit()
