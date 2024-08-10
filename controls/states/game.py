import pygame as pg

import constants as c
from controls.states.state import State
from controls.states.pausemenu import PauseMenu
from objects.ball.ball import Ball
from objects.blocks.blockmanager import BlockManager
from objects.paddle.bat import Bat
from ui.ui import UI


def initialize(grid_size: tuple[int, int]):
    return Bat(), Ball(), BlockManager(grid_size), UI()


class MainGame(State):
    def __init__(self,
                 grid_size: tuple[int, int] = (c.target_columns, c.target_rows)):

        # Game objects
        self.bat, self.ball, self.block_manager, self.ui = initialize(grid_size)

        self.keys = pg.key.get_pressed()
        self.prev_keys = self.keys

    def auto_play(self):
        self.bat.pos.x = self.ball.pos.x - self.ball.radius

    # Game loop
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                c.game_state = []
            if event.type == pg.MOUSEBUTTONDOWN:
                self.handle_mouse_click()

    def handle_mouse_click(self):
        mouse_pos = pg.mouse.get_pos()
        self.debug_destroy_target_block(mouse_pos)

    def handle_key_presses(self):
        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_ESCAPE] and not self.prev_keys[pg.K_ESCAPE]:
            c.game_state.append(PauseMenu())
        if self.keys[pg.K_q]:
            c.game_state.pop(-1)
        self.prev_keys = self.keys

    def debug_destroy_target_block(self,
                                   mouse_pos: tuple[int, int]):
        for column in self.block_manager.target_blocks:
            for block in column:
                if block is not None and block.pos.collides_with_point(mouse_pos):
                    self.block_manager.target_hit_by_ball(block)

    def update_game(self):
        if self.bat.swing_timer.ready:
            if self.keys[pg.K_SPACE]:
                self.bat.swing(self.ball)
        self.bat.update(self.keys)
        # This will be True if the ball hits the bottom of the window
        if self.ball.update(self.block_manager) is not None:
            self.reset_game()
            return
        self.block_manager.update()
        self.prev_keys = self.keys

    def reset_game(self):
        grid_size = (self.block_manager.target_columns, self.block_manager.target_rows)
        self.bat, self.ball, self.block_manager, self.ui = initialize(grid_size)

    def draw_game(self):
        c.window.fill((50, 50, 50))
        self.block_manager.draw()
        self.ball.draw()
        self.bat.draw()
        self.ui.draw(self.bat, self.block_manager, c.window)
        pg.display.update()

    def run(self):
        self.handle_events()
        self.handle_key_presses()
        self.update_game()
        self.draw_game()
        c.clock.tick(c.FPS)
