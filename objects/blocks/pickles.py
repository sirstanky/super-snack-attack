from random import random

import constants as c
from objects.blocks.block import CaughtBlock, FallingBlock, TargetBlock
from sprites.spritesheet import SpriteSheet

caught_info = 'assets/blocks/pickle/caught.png', [1]
falling_info = 'assets/blocks/pickle/falling.png', [1]
target_info = 'assets/blocks/pickle/target.png', [1]


class PickleCaught(CaughtBlock):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float] = c.caught_block_size,
                 score_value: int = c.pickle_score):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(caught_info, size),
                         score_value=score_value)


class PickleFalling(FallingBlock):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 max_speed: float = c.pickle_fall_speed,
                 speed: tuple[float, float] = (0.0, 0.0),
                 acceleration: float = c.pickle_fall_acceleration):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(falling_info, size),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration)

    def on_catch(self):
        return [PickleCaught(center=self.pos.center)]

    def update(self):
        speed_x = self.speed_x
        self.accelerate((0, 1), cap_speed=False)
        if self.speed_y > self.max_speed:
            self.speed_y = self.max_speed
        self.move()
        self.speed_x = speed_x
        if self.pos.left < 0 or self.pos.right > c.window_width:
            self.speed_x *= -1


class PickleTarget(TargetBlock):
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
        def decide_speed():
            speed_x = self.max_speed * random()
            speed_y = -(self.max_speed - speed_x)
            if random() < 0.5:
                speed_x *= -1
            return speed_x, speed_y

        return [PickleFalling(center=self.pos.center,
                              size=self.pos.size,
                              speed=decide_speed()) for _ in range(3)]
