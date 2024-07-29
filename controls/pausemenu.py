import pygame as pg
from pygame.font import Font

import constants as c


class PauseMenu:
    def __init__(self):
        self.font = Font('freesansbold.ttf', 16)
        self.text = self.font.render("Paused", True, (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.center = c.window_width / 2, c.window_height / 2
        self.active = True

    def start(self):
        screen_shot = pg.Surface((c.window_width, c.window_height))
        screen_shot.blit(c.window, (0, 0), pg.Rect(0, 0, c.window_width, c.window_height))
        result = self.running(screen_shot)
        return result

    def running(self,
                screen_shot: pg.Surface):
        while self.active:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'quit'
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                return 'play'
            self.draw(screen_shot)

    def draw(self,
             screen_shot: pg.Surface):
        c.window.fill((0, 0, 0))
        c.window.blit(screen_shot, (0, 0))
        c.window.blit(self.text, self.rect)
        pg.display.update()

