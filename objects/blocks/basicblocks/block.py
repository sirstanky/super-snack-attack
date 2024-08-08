from enum import Enum

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

    def update(self,
               **kwargs):
        if self.state.value == Block.State.TARGET:
            if self.y_destination is not None:
                self.accelerate((0, 1))
                self.move()
                if self.pos.y >= self.y_destination:
                    self.pos.y = self.y_destination
                    self.y_destination = None
                    self.speed_y = 0.0

        elif self.state.value == Block.State.FALLING:
            self.accelerate((0, 1))
            self.move()

        elif self.state.value == Block.State.CAUGHT:
            self.pos.center = kwargs['caught_position']

    # TODO This will have to be written to handle different sprite states and animations
    def draw(self):
        self.sprite.draw(self.pos.center, self.state.value)
