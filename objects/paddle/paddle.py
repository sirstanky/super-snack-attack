from objects.basicobject import BasicObject
from sprites.spritesheet import SpriteSheet


class Paddle(BasicObject):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 sprite_sheet: SpriteSheet,
                 max_speed: float,
                 speed: tuple[float, float],
                 acceleration: float):
        super().__init__(center=center,
                         size=size,
                         sprite_sheet=sprite_sheet,
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration)

    def update(self,
               **kwargs):
        super().update()
