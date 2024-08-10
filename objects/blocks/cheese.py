import constants as c
from objects.blocks.block import Block
from sprites.spritesheet import SpriteSheet


class Cheese(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 max_speed: float = None,
                 speed: tuple[float, float] = (0.0, 0.0),
                 acceleration: float = None,
                 score_value: int = None,
                 state: Block.State = None,
                 y_destination: float = None):

        if max_speed is None:
            max_speed = c.falling_block_speed
        if acceleration is None:
            acceleration = c.falling_block_acceleration
        if score_value is None:
            score_value = 10  # TODO Move this to 'constants'

        # TODO Load sprite
        sprite = SpriteSheet('assets/cheese.png', size, (32, 32), [1, 1, 1])

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=sprite,
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration,
                         score_value=score_value,
                         state=state,
                         y_destination=y_destination)
