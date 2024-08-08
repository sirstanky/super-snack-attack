from math import pi, sin
from random import random

import constants as c
from objects.blocks.basicblocks.fallingblock import FallingBlock
from sprites.sprite import Sprite


class FloatingBlock(FallingBlock):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 color: tuple[int, int, int] = None,
                 speed: float = None,
                 swing_distance: float = None,
                 drop_distance: float = None,
                 sprite_sheet: Sprite = None):
        if speed is None:
            speed = c.floating_block_speed
        if swing_distance is None:
            swing_distance = c.floating_block_swing_distance
        if drop_distance is None:
            drop_distance = c.floating_block_swing_distance

        super().__init__(center,
                         size,
                         color,
                         speed,
                         sprite_sheet=sprite_sheet)

        self.swing_distance = swing_distance
        self.drop_dist = drop_distance
        self.float_time = c.clock.get_time() / 1000

        self.y_limit = self.pos.y
        self.center_line = self.pos.x
        self.count = 0

        self.quarter_swing = (self.swing_distance / 2)
        self.reverse_time = self.find_reversal_time()

        if random() < 0.5:
            self.para_start = self.left_swing - self.quarter_swing
            self.para_end = self.center_line
            self.dir = -1
        else:
            self.para_start = self.center_line
            self.para_end = self.right_swing + self.quarter_swing
            self.dir = 1

    @property
    def right_swing(self):
        return self.center_line + self.swing_distance

    @property
    def left_swing(self):
        return self.center_line - self.swing_distance

    def find_parabola(self):
        if self.pos.x < self.center_line:
            self.para_start = self.left_swing
            self.para_end = self.right_swing + self.quarter_swing
        else:
            self.para_start = self.left_swing - self.quarter_swing
            self.para_end = self.right_swing
        self.y_limit += self.pos.y - self.y_limit

    def find_reversal_time(self):
        new_time = (1 / (pi * self.max_speed)) * ((pi / 2) + (self.count * pi))
        return new_time

    def update(self):
        def find_parabola():
            if self.pos.x < self.center_line:
                self.para_start = self.left_swing
                self.para_end = self.right_swing + self.quarter_swing
            else:
                self.para_start = self.left_swing - self.quarter_swing
                self.para_end = self.right_swing
            self.y_limit += self.pos.y - self.y_limit

        self.float_time += c.clock.get_time() / 1000  # TODO Change to a local timer so as not to be affected by pausing
        self.pos.x = self.dir * self.swing_distance * sin(pi * self.max_speed * self.float_time) + self.center_line
        if self.float_time > self.reverse_time:
            self.count += 1
            self.reverse_time = self.find_reversal_time()
            self.find_parabola()
        vertex = (self.para_start + self.para_end) / 2
        amp = self.drop_dist / ((vertex - self.para_start) * (vertex - self.para_end))
        self.pos.y = amp * (self.pos.x - self.para_start) * (self.pos.x - self.para_end) + self.y_limit
