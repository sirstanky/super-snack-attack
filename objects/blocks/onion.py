import constants as c
from objects.blocks.block import CaughtBlock, FallingBlock, TargetBlock
from sprites.spritesheet import SpriteSheet

caught_info = 'assets/blocks/onion/caught.png', [1]
falling_info = 'assets/blocks/onion/falling.png', [1, 1]
target_info = 'assets/blocks/onion/target.png', [1]


class OnionCaught(CaughtBlock):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float] = c.caught_block_size,
                 score_value: int = c.onion_score):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(caught_info, size),
                         score_value=score_value)


class OnionFalling(FallingBlock):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 max_speed: float = c.onion_fall_speed,
                 speed: tuple[float, float] = (0.0, 0.0),
                 acceleration: float = c.onion_fall_acceleration):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(falling_info, size),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration)

        self.sliced = False

    def hit_by_bat(self):
        self.sliced = True
        self.sprite.next_sprite()

    def on_catch(self):
        if self.sliced:
            return [OnionCaught(center=self.pos.center)]
        # TODO Make method to 'bounce' off the sandwich.
        return None


class OnionTarget(TargetBlock):
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
        return [OnionFalling(center=self.pos.center,
                             size=self.pos.size,
                             speed=self.speed)]
