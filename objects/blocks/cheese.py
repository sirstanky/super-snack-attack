import constants as c
from objects.blocks.block import Block
from sprites.spritesheet import SpriteSheet


class Cheese(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 max_speed: float = c.falling_block_speed,
                 speed: tuple[float, float] = (0.0, 0.0),
                 acceleration: float = c.falling_block_acceleration,
                 score_value: int = 10,
                 state: Block.State = None,
                 y_destination: float = None):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet('assets/cheese.png', size, (32, 32), [1, 1, 1]),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration,
                         score_value=score_value,
                         state=state,
                         y_destination=y_destination)
