import constants as c
from objects.blocks.block import Block
from sprites.spritesheet import SpriteSheet


class Onion(Block):
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
                         sprite_sheet=SpriteSheet('assets/onion.png', size, (32, 32), [1, 1, 1]),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration,
                         score_value=score_value,
                         state=state,
                         y_destination=y_destination)

        self.falling_sprite = 0
        self.sliced = False

    def hit_by_bat(self):
        self.sliced = True
        self.sprite.next_sprite()

    def on_catch(self):
        return self.sliced
