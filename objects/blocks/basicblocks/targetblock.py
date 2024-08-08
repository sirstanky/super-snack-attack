from random import randint

import constants as c
from objects.blocks.basicblocks.block import Block


def random_color():
    r = randint(0, 253)
    g = randint(0, 254 - r)
    b = 255 - r - g
    return r, g, b


class TargetBlock(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 color: tuple[int, int, int] = None,
                 max_speed: float = None,
                 acceleration: float = None,
                 dest_y: float = None):
        if color is None:
            color = random_color()
        if max_speed is None:
            max_speed = c.target_block_speed
        if acceleration is None:
            acceleration = c.target_block_acceleration

        super().__init__(center,
                         size,
                         color,
                         max_speed,
                         acceleration=acceleration)

        self.dest_y = dest_y

    def set_destination(self,
                        new_dest_y: float):
        if self.pos.y != new_dest_y:
            self.dest_y = new_dest_y

    def update(self):
        super().update()
        if self.dest_y is not None:
            self.accelerate((0, 1))
            if self.pos.y >= self.dest_y:
                self.pos.y = self.dest_y
                self.dest_y = None
                self.speed_y = 0
        else:
            self.accelerate((0, 0))
