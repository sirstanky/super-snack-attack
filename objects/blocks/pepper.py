import constants as c
from objects.blocks.block import CaughtBlock, FallingBlock, TargetBlock
from sprites.spritesheet import SpriteSheet

caught_info = 'assets/blocks/pepper/caught.png', [1]
falling_info = 'assets/blocks/pepper/falling.png', [1]
target_info = 'assets/blocks/pepper/target.png', [1, 1, 1]


class PepperCaught(CaughtBlock):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float] = c.caught_block_size,
                 score_value: int = c.pepper_score):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(caught_info, size),
                         score_value=score_value)


class PepperFalling(FallingBlock):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 max_speed: float = c.pepper_fall_speed,
                 speed: tuple[float, float] = (0.0, 0.0),
                 acceleration: float = c.pepper_fall_acceleration):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(falling_info, size),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration)

    def on_catch(self):
        return [PepperCaught(center=self.pos.center)]


class PepperTarget(TargetBlock):
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

        self.hits = 3

    def on_hit(self):
        self.hits -= 1
        if self.hits > 0:
            self.sprite.next_sprite()
        else:
            return [PepperFalling(center=self.pos.center,
                                  size=self.pos.size,
                                  speed=self.speed)]
