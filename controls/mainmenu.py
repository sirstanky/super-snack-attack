import pygame as pg
from pygame.font import Font

import constants as c


class MainMenu:
    def __init__(self):
        self.font_title = Font('freesansbold.ttf', 32)
        self.text_title = self.font_title.render("Super Snack Attack", True, (255, 255, 255))
        self.rect_title = self.text_title.get_rect()
        self.rect_title.center = c.window_width / 2, c.window_height / 4
        self.font_button = Font('freesansbold.ttf', 16)
        self.text_button = self.font_button.render("Play Game", True, (255, 255, 255))
        self.rect_button = self.text_button.get_rect()
        self.rect_button.center = c.window_width / 2, c.window_height / 2
        self.active = True

    def running(self):
        while self.active:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'quit'
                if event.type == pg.MOUSEBUTTONDOWN and self.rect_button.collidepoint(pg.mouse.get_pos()):
                    return 'play'
            self.draw()

    def draw(self):
        c.window.fill((0, 0, 0))
        c.window.blit(self.text_title, self.rect_title)
        c.window.blit(self.text_button, self.rect_button)
        pg.display.update()
