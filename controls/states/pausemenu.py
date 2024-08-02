import pygame as pg
from pygame.font import Font

import constants as c
from controls.states.state import State


class PauseMenu(State):
    def __init__(self):
        self.font = Font('freesansbold.ttf', 16)
        self.text = self.font.render("Paused", True, (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.center = c.window_width / 2, c.window_height / 2
        self.screen_shot = pg.Surface((c.window_width, c.window_height))
        self.screen_shot.blit(c.window, (0, 0), pg.Rect(0, 0, c.window_width, c.window_height))
        self.keys = pg.key.get_pressed()
        self.prev_keys = pg.key.get_pressed()

    def run(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                c.game_state = []
        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_ESCAPE] and not self.prev_keys[pg.K_ESCAPE]:
            c.game_state.pop(-1)
        self.prev_keys = self.keys
        self.draw()

    def draw(self):
        c.window.fill((0, 0, 0))
        c.window.blit(self.screen_shot, (0, 0))
        c.window.blit(self.text, self.rect)
        pg.display.update()
