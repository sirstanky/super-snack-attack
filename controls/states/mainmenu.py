import pygame as pg
from pygame.font import Font

import constants as c
from controls.states.state import State
from controls.states.game import MainGame


class MainMenu(State):
    def __init__(self):
        self.font_title = Font('freesansbold.ttf', 32)
        self.text_title = self.font_title.render("Super Snack Attack", True, (255, 255, 255))
        self.rect_title = self.text_title.get_rect()
        self.rect_title.center = c.window_width / 2, c.window_height / 4
        self.font_button = Font('freesansbold.ttf', 16)
        self.text_button = self.font_button.render("Play Game", True, (255, 255, 255))
        self.rect_button = self.text_button.get_rect()
        self.rect_button.center = c.window_width / 2, c.window_height / 2
        self.draw_rect = pg.Rect(self.rect_button.x - 2, self.rect_button.y - 2, self.rect_button.w + 4,
                                 self.rect_button.h + 4)

    def run(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                c.game_state = []
            if event.type == pg.MOUSEBUTTONDOWN and self.rect_button.collidepoint(pg.mouse.get_pos()):
                c.game_state.append(MainGame())
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                c.game_state = []
        self.draw()

    def draw(self):
        c.window.fill((0, 0, 0))
        c.window.blit(self.text_title, self.rect_title)
        c.window.blit(self.text_button, self.rect_button)
        pg.draw.rect(c.window, (255, 255, 255), self.draw_rect, width=1)
        pg.display.update()
