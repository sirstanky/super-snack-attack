from pygame import Rect

import constants as c
from objects.blocks.basicblocks.basicblock import BasicBlock


class FallingBlock(BasicBlock):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 color: tuple[int, int, int],
                 max_speed: float = None,
                 speed: tuple[float, float] = None,
                 acceleration: float = None):
        if max_speed is None:
            max_speed = c.falling_block_speed
        if speed is None:
            speed = (0.0, 0.0)
        if acceleration is None:
            acceleration = c.falling_block_acceleration

        super().__init__(center,
                         size,
                         color,
                         max_speed,
                         speed=speed,
                         acceleration=acceleration)

    @property
    def catch_area(self):
        return Rect(self.pos.left, self.pos.y, self.pos.width, self.pos.height / 2)

    def update(self):
        self.accelerate((0, 1))
        super().update()
