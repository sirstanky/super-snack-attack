from enum import Enum
from random import random

import constants as c
from objects.basicobject import BasicObject
from objects.position import Position
from sprites.spritesheet import SpriteSheet


class State(Enum):
    TARGET = 0
    FALLING = 1
    CAUGHT = 2
    DROPPED = 3


def get_state_speeds(state: State):
    if state == State.TARGET:
        return c.target_block_max_speed, c.target_block_acceleration
    elif state == State.FALLING:
        return c.target_block_max_speed, c.target_block_acceleration
    elif state == State.CAUGHT:
        return (0.0, 0.0), 0.0
    elif state == State.DROPPED:
        return c.target_block_max_speed, c.target_block_acceleration
    else:
        raise Exception(f"Passed invalid state \'{state}\'")


class Block(BasicObject):

    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 sprite_sheet: SpriteSheet,
                 max_speed: float,
                 speed: tuple[float, float],
                 acceleration: float,
                 score_value: int,
                 target_y_dest: float = None,
                 state: State = State.TARGET):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=sprite_sheet,
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration)

        self.score_value = score_value
        self.target_y_dest = target_y_dest
        self.state = state

    @property
    def catch_area(self):
        return Position((self.pos.x, self.pos.y + self.pos.height / 4), (self.pos.width, self.pos.height / 2))

    def change_state(self,
                     state: State):
        if state == State.CAUGHT:
            self.pos.size = c.caught_block_size
        elif state == State.DROPPED:
            self.pos.size = c.block_size
        self.state = state

    def on_hit(self):
        self.change_state(State.FALLING)
        return True

    def hit_by_bat(self):
        pass

    def on_catch(self,
                 **kwargs):
        self.change_state(State.CAUGHT)
        return True

    def set_knock_speed(self):
        self.speed_x = self.max_speed * random()
        self.speed_y = -(self.max_speed - self.speed_x)
        if random() < 0.5:
            self.speed_x *= -1

    def knock_off(self):
        self.set_knock_speed()

    def fall_at_angle(self):
        speed_x = self.speed_x
        self.accelerate((0, 1), cap_speed=False)
        if self.speed_y > self.max_speed:
            self.speed_y = self.max_speed
        self.move()
        self.speed_x = speed_x
        if self.pos.left < 0 or self.pos.right > c.window_width:
            self.speed_x *= -1

    def target_update(self):
        if self.target_y_dest is not None:
            self.accelerate((0, 1))
            self.move()
            if self.pos.y >= self.target_y_dest:
                self.pos.y = self.target_y_dest
                self.target_y_dest = None
                self.speed_y = 0.0

    def falling_update(self):
        self.accelerate((0, 1))
        self.move()

    def caught_update(self,
                      catcher_position: tuple[float, float],
                      stack_layer: int):
        self.pos.x = catcher_position[0]
        self.pos.y = catcher_position[1] - self.pos.height * stack_layer - self.pos.height / 2

    def dropped_update(self):
        self.fall_at_angle()

    def update(self,
               catcher_position: tuple[float, float],
               stack_layer: int):
        if self.state == State.TARGET:
            self.target_update()
        elif self.state == State.FALLING:
            self.falling_update()
        elif self.state == State.CAUGHT:
            self.caught_update(catcher_position, stack_layer)
        elif self.state == State.DROPPED:
            self.dropped_update()
