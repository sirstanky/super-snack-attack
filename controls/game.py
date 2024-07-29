import pygame as pg

import constants as c
from objects.ball.ball import Ball
from blockmanagers.blockmanager import BlockManager
from objects.paddle.bat import Bat
from objects.paddle.catcher import Catcher
from ui.ui import UI

# Key states
keys = pg.key.ScancodeWrapper
prev_keys = keys


def initialize(grid_size: tuple[int, int] = None):
    if grid_size is None:
        grid_size = (c.target_columns, c.target_rows)
    return Bat(), Catcher(), Ball(), BlockManager(grid_size), UI()


class MainGame:
    def __init__(self,
                 grid_size: tuple[int, int] = None):
        if grid_size is None:
            grid_size = (c.target_columns, c.target_rows)

        # Game objects
        self.bat, self.catcher, self.ball, self.block_manager, self.ui = initialize(grid_size)

        self.running = True

    def auto_play(self):
        self.bat.pos.x = self.ball.pos.x - self.ball.radius

    # Game loop
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                continue
            if event.type == pg.MOUSEBUTTONDOWN:
                self.handle_mouse_click()

    def handle_mouse_click(self):
        mouse_pos = pg.mouse.get_pos()
        self.debug_reduce_caught_blocks(mouse_pos)
        self.debug_destroy_target_block(mouse_pos)

    def debug_reduce_caught_blocks(self,
                                   mouse_pos: tuple[int, int]):
        caught_blocks = self.catcher.caught_manager.blocks
        if caught_blocks:
            w = caught_blocks[0].pos.width
            h = caught_blocks[0].pos.height * min(len(caught_blocks), self.catcher.caught_manager.display_limit)
            x, y = caught_blocks[-1].pos.top_left
            sandwich = pg.Rect(x, y, w, h)
            if sandwich.collidepoint(mouse_pos):
                while len(caught_blocks) > self.catcher.caught_manager.display_limit / 2:
                    caught_blocks.pop(-1)

    def debug_destroy_target_block(self,
                                   mouse_pos: tuple[int, int]):
        for column in self.block_manager.target_manager.columns:
            for block in column.blocks:
                if block is not None and block.pos.collides_with_point(mouse_pos):
                    self.block_manager.block_hit_by_ball(block)

    def update_game(self):
        global keys, prev_keys
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            return 'paused'
        if self.bat.swing_timer.ready:
            if keys[pg.K_SPACE] and not prev_keys[pg.K_SPACE]:
                self.bat.swing(self.ball)
        accel = [0, 0]
        if self.bat.swing_timer.ready:
            if keys[pg.K_UP]:
                accel[1] -= 1
            if keys[pg.K_DOWN]:
                accel[1] += 1
            if keys[pg.K_LEFT] and self.bat.pos.x > -(self.bat.pos.width / 5):
                accel[0] -= 1
            if keys[pg.K_RIGHT] and self.bat.pos.x + ((self.bat.pos.width / 5) * 4) < c.window_width:
                accel[0] += 1
        self.bat.accelerate((accel[0], accel[1]))
        self.bat.update()
        # This will be True if the ball hits the bottom of the window
        if self.ball.update(self.block_manager) is not None:
            self.reset_game()
            return
        self.block_manager.update()
        self.catcher.update(self.block_manager.falling_manager)
        prev_keys = keys

    def reset_game(self):
        grid_size = (self.block_manager.target_manager.num_columns, self.block_manager.target_manager.num_rows)
        self.running = True
        self.bat, self.catcher, self.ball, self.block_manager, self.ui = initialize(grid_size)

    def draw_game(self):
        c.window.fill((50, 50, 50))
        self.catcher.draw(c.window)
        self.block_manager.draw(c.window)
        self.ball.draw(c.window)
        self.bat.draw(c.window)
        self.ui.draw(self.bat, self.catcher, self.block_manager.target_manager, c.window)
        pg.display.update()

    def play(self):
        while self.running:
            self.handle_events()
            _ = self.update_game()
            if _ is not None:
                return _
            self.draw_game()
            c.clock.tick(c.FPS)
        return 'quit'
