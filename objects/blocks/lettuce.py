from math import pi, sin
from random import random

import constants as c
from objects.blocks.block import Block, State, get_state_speeds
from sprites.spritesheet import SpriteSheet, get_image_and_frames

sprite_frames = [1, 1, 1, 1]
sprite_sheet, frame_size = get_image_and_frames('assets/blocks/lettuce.png', sprite_frames)


def get_lettuce_speeds(state: State):
    if state == State.FALLING:
        return c.lettuce_fall_speed, c.lettuce_fall_acceleration
    else:
        return get_state_speeds(state)


class Lettuce(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 speed: tuple[float, float] = (0.0, 0.0),
                 score_value = c.lettuce_score,
                 target_y_dest: float = None,
                 state: State = State.TARGET,
                 swing_distance: float = c.lettuce_swing_distance,
                 drop_distance: float = c.lettuce_drop_distance):

        max_speed, acceleration = get_lettuce_speeds(state)

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(sprite_sheet, frame_size, sprite_frames, size),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration,
                         score_value=score_value,
                         target_y_dest=target_y_dest,
                         state=state)

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
        vertex = (self.para_start + self.para_end) / 2
        self.amp = (self.drop_distance / ((vertex - self.para_start) * (vertex - self.para_end))) / 2

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
                     state: State):
        self.max_speed, self.acceleration = get_lettuce_speeds(state)
        self.sprite.change_sprite(state.value)
        super().change_state(state)

    def on_hit(self):
        self.swing_height_limit = self.pos.y
        return super().on_hit()

    def find_reversal_time(self):
        return (1 / (pi * c.lettuce_fall_speed)) * ((pi / 2) + (self.swing_count * pi))

    def update(self,
               catcher_position: tuple[float, float],
               stack_layer: int):
        def find_parabola():
            if self.pos.x < self.center_line:
                self.para_start = self.left_swing
                self.para_end = self.right_swing + self.quarter_swing
            else:
                self.para_start = self.left_swing - self.quarter_swing
                self.para_end = self.right_swing
            self.swing_height_limit = self.pos.y
            vertex = (self.para_start + self.para_end) / 2
            self.amp = self.drop_distance / ((vertex - self.para_start) * (vertex - self.para_end))

        if self.state != State.FALLING:
            super().update(catcher_position, stack_layer)
            return

        self.float_time += self.acceleration
        self.pos.x = self.dir * self.swing_distance * sin(pi * self.max_speed * self.float_time) + self.center_line
        if self.float_time > self.reversal_time:
            self.swing_count += 1
            self.reversal_time = self.find_reversal_time()
            find_parabola()
        self.pos.y = self.amp * (self.pos.x - self.para_start) * (self.pos.x - self.para_end) + self.swing_height_limit
