from __future__ import annotations
from enum import Enum

import constants as c
from objects.basicobject import BasicObject
from sprites.spritesheet import SpriteSheet
from objects.position import Position


class Block(BasicObject):
    class State(Enum):
        TARGET = 0
        FALLING = 1
        CAUGHT = 2

    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 sprite_sheet: SpriteSheet,
                 max_speed: float,
                 speed: tuple[float, float],
                 acceleration: float,
                 score_value: int,
                 state: State = None,
                 y_destination: float = None):
        super().__init__(center=center,
                         size=size,
                         sprite_sheet=sprite_sheet,
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration, )
        if state is None:
            self.state = Block.State.TARGET
        else:
            self.state = state

        self.score_value = score_value
        self.y_destination = y_destination

    @property
    def catch_area(self):
        return Position((self.pos.x, self.pos.y + self.pos.height / 4), (self.pos.width, self.pos.height / 2))

    def change_state(self,
                     state: Block.State,
                     **kwargs):
        self.state = state
        self.sprite.current_sprite = self.sprite.sprites[state.value]
        if state == Block.State.TARGET:
            if 'y_destination' in kwargs:
                self.y_destination = kwargs['y_destination']
        elif state == Block.State.FALLING:
            pass
        elif state == Block.State.CAUGHT:
            pass

    def update(self,
               **kwargs):
        if self.state.value == Block.State.TARGET.value:
            if self.y_destination is not None:
                self.accelerate((0, 1))
                self.move()
                if self.pos.y >= self.y_destination:
                    self.pos.y = self.y_destination
                    self.y_destination = None
                    self.speed_y = 0.0

        elif self.state.value == Block.State.FALLING.value:
            self.accelerate((0, 1))
            self.move()

        elif self.state.value == Block.State.CAUGHT.value:
            self.pos.x = kwargs['catcher_position'].x
            self.pos.y = kwargs['catcher_position'].y - c.caught_block_size[1] * kwargs['layer'] - self.pos.height / 2

    # TODO This will have to be written to handle different sprite states and animations
    def draw(self):
        self.sprite.draw(self.pos)
