from math import pi, sin
from random import random

import constants as c
from objects.blocks.block import Block
from sprites.spritesheet import SpriteSheet


class Lettuce(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 max_speed: float = None,
                 speed: tuple[float, float] = (0.0, 0.0),
                 acceleration: float = None,
                 score_value: int = 30,
                 state: Block.State = None,
                 y_destination: float = None,
                 swing_distance: float = c.floating_block_swing_distance,
                 drop_distance: float = c.floating_block_drop_distance):

        if max_speed is None:
            if state is None:
                max_speed = c.falling_block_speed
            else:
                max_speed = c.floating_block_speed
        if acceleration is None:
            if state is None:
                acceleration = c.falling_block_acceleration
            else:
                acceleration = c.floating_block_acceleration

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet('assets/lettuce.png', size, (32, 32), [1, 1, 1]),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration,
                         score_value=score_value,
                         state=state,
                         y_destination=y_destination)

        self.swing_distance = swing_distance
        self.drop_distance = drop_distance
        self.swing_height_limit = 0
        self.center_line = self.pos.x
        self.swing_count = 0
        self.reversal_time = self.find_reversal_time()
        self.float_time = 0
        self.para_start = None
        self.para_end = None
        self.dir = None

    @property
    def quarter_swing(self):
        return self.swing_distance / 2

    @property
    def right_swing(self):
        return self.center_line + self.swing_distance

    @property
    def left_swing(self):
        return self.center_line - self.swing_distance

    def change_state(self,
                     state: Block.State,
                     **kwargs):
        if state == Block.State.FALLING:
            self.max_speed = c.floating_block_speed
            self.acceleration = c.floating_block_acceleration
            self.swing_height_limit = self.pos.y
        if random() < 0.5:
            self.para_start = self.center_line
            self.para_end = self.left_swing - self.quarter_swing
            self.dir = -1
        else:
            self.para_start = self.center_line
            self.para_end = self.right_swing + self.quarter_swing
            self.dir = 1
        super().change_state(state)

    def find_reversal_time(self):
        return (1 / (pi * c.floating_block_speed)) * ((pi / 2) + (self.swing_count * pi))

    def update(self,
               **kwargs):
        def update_fall():
            def find_parabola():
                if self.pos.x < self.center_line:
                    self.para_start = self.left_swing
                    self.para_end = self.right_swing + self.quarter_swing
                else:
                    self.para_start = self.left_swing - self.quarter_swing
                    self.para_end = self.right_swing
                self.swing_height_limit = self.pos.y

            self.float_time += self.acceleration
            self.pos.x = self.dir * self.swing_distance * sin(pi * self.max_speed * self.float_time) + self.center_line
            if self.float_time > self.reversal_time:
                self.swing_count += 1
                self.reversal_time = self.find_reversal_time()
                find_parabola()
            vertex = (self.para_start + self.para_end) / 2
            amp = self.drop_distance / ((vertex - self.para_start) * (vertex - self.para_end))
            if self.swing_count == 0:
                amp /= 2
            self.pos.y = amp * (self.pos.x - self.para_start) * (self.pos.x - self.para_end) + self.swing_height_limit

        if self.state.value == Block.State.TARGET.value:
            super().update()
        elif self.state.value == Block.State.FALLING.value:
            update_fall()
        elif self.state.value == Block.State.CAUGHT.value:
            super().update(catcher_position=kwargs['catcher_position'], layer=kwargs['layer'])
            
    def draw(self):
        super().draw()
