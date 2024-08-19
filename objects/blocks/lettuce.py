from math import pi, sin
from random import random

import constants as c
from objects.blocks.block import CaughtBlock, FallingBlock, TargetBlock
from sprites.spritesheet import SpriteSheet

caught_info = 'assets/blocks/lettuce/caught.png', [1]
falling_info = 'assets/blocks/lettuce/falling.png', [1]
target_info = 'assets/blocks/lettuce/target.png', [1]


class LettuceCaught(CaughtBlock):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float] = c.caught_block_size,
                 score_value: int = c.lettuce_score):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(caught_info, size),
                         score_value=score_value)


class LettuceFalling(FallingBlock):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 max_speed: float = c.lettuce_fall_speed,
                 speed: tuple[float, float] = (0.0, 0.0),
                 acceleration: float = c.lettuce_fall_acceleration,
                 swing_distance: float = c.lettuce_swing_distance,
                 drop_distance: float = c.lettuce_drop_distance):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(falling_info, size),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration)

        self.swing_distance = swing_distance
        self.drop_distance = drop_distance
        self.swing_height_limit = self.pos.y
        self.center_line = self.pos.x
        self.swing_count = 0
        self.reversal_time = self.find_reversal_time()
        self.float_time = 0
        if random() < 0.5:
            self.para_start = self.center_line
            self.para_end = self.left_swing - self.quarter_swing
            self.dir = -1
        else:
            self.para_start = self.center_line
            self.para_end = self.right_swing + self.quarter_swing
            self.dir = 1

    @property
    def quarter_swing(self):
        return self.swing_distance / 2

    @property
    def right_swing(self):
        return self.center_line + self.swing_distance

    @property
    def left_swing(self):
        return self.center_line - self.swing_distance

    def on_catch(self):
        return [LettuceCaught(center=self.pos.center)]

    def find_reversal_time(self):
        return (1 / (pi * c.floating_block_speed)) * ((pi / 2) + (self.swing_count * pi))

    def update(self):
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


class LettuceTarget(TargetBlock):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 max_speed: float = None,
                 acceleration: float = None,
                 y_destination: float = None):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(target_info, size),
                         max_speed=max_speed,
                         acceleration=acceleration,
                         y_destination=y_destination)

    def on_hit(self):
        return [LettuceFalling(center=self.pos.center,
                               size=self.pos.size,
                               speed=self.speed)]
