import constants as c
from objects.blocks.block import Block
from sprites.spritesheet import SpriteSheet


class Pepper(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 max_speed: float = c.falling_block_speed,
                 speed: tuple[float, float] = (0.0, 0.0),
                 acceleration: float = c.falling_block_acceleration,
                 score_value: int = 50,
                 state: Block.State = None,
                 y_destination: float = None):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet('assets/pepper.png', size, (32, 32), [1, 1, 1, 1, 1]),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration,
                         score_value=score_value,
                         state=state,
                         y_destination=y_destination)

        self.hits = 3

    def on_hit(self):
        self.hits -= 1
        self.sprite.next_sprite()
        if self.hits <= 0:
            return True
