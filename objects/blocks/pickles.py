from random import random

import constants as c
from objects.blocks.block import Block
from sprites.spritesheet import SpriteSheet


class Pickles(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 max_speed: float = c.falling_block_speed,
                 speed: tuple[float, float] = (0.0, 0.0),
                 acceleration: float = c.falling_block_acceleration * 0.75,
                 score_value: int = 20,
                 state: Block.State = None,
                 y_destination: float = None
                 ):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet('assets/pickles.png', size, (32, 32), [1, 1, 1]),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration,
                         score_value=score_value,
                         state=state,
                         y_destination=y_destination)

    def change_state(self,
                     state: Block.State,
                     **kwargs):
        def decide_speed():
            speed_x = self.max_speed * random()
            speed_y = -(self.max_speed - speed_x)
            if random() < 0.5:
                speed_x *= -1
            return speed_x, speed_y

        if state == Block.State.FALLING:
            self.state = state
            self.sprite.change_sprite(Block.State.FALLING.value)
            self.speed_x, self.speed_y = decide_speed()
            block1 = Pickles(center=self.pos.center,
                             size=self.pos.size,
                             max_speed=self.max_speed,
                             speed=decide_speed(),
                             acceleration=self.acceleration,
                             score_value=self.score_value,
                             state=Block.State.FALLING)
            block1.sprite.change_sprite(Block.State.FALLING.value)
            block2 = Pickles(center=self.pos.center,
                             size=self.pos.size,
                             max_speed=self.max_speed,
                             speed=decide_speed(),
                             acceleration=self.acceleration,
                             score_value=self.score_value,
                             state=Block.State.FALLING)
            block2.sprite.change_sprite(Block.State.FALLING.value)
            kwargs['falling_blocks'].append(block1)
            kwargs['falling_blocks'].append(block2)
        else:
            super().change_state(state)

    def update(self,
               **kwargs):
        if self.state == Block.State.TARGET:
            super().update()
        elif self.state == Block.State.FALLING:
            speed_x = self.speed_x
            self.accelerate((0, 1), cap_speed=False)
            if self.speed_y > self.max_speed:
                self.speed_y = self.max_speed
            self.move()
            self.speed_x = speed_x
            if self.pos.left < 0 or self.pos.right > c.window_width:
                self.speed_x *= -1
        elif self.state == Block.State.CAUGHT:
            super().update(catcher_position=kwargs['catcher_position'], layer=kwargs['layer'])
