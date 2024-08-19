import constants as c
from objects.basicobject import BasicObject
from objects.position import Position
from sprites.spritesheet import SpriteSheet


class Block(BasicObject):

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


class CaughtBlock(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 sprite_sheet: SpriteSheet,
                 score_value: int):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=sprite_sheet,
                         max_speed=0.0,
                         speed=(0, 0),
                         acceleration=0.0)

        self.score_value = score_value

    def update(self,
               position: tuple[float, float],
               stack_layer: int):
        self.pos.x = position[0]
        self.pos.y = position[1] - self.pos.height * stack_layer - self.pos.height / 2


class FallingBlock(Block):
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

    @property
    def catch_area(self):
        return Position((self.pos.x, self.pos.y + self.pos.height / 4), (self.pos.width, self.pos.height / 2))

    def hit_by_bat(self):
        pass

    def on_catch(self):
        return True

    def update(self):
        self.accelerate((0, 1))
        self.move()


class TargetBlock(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 sprite_sheet: SpriteSheet,
                 max_speed: float,
                 acceleration: float,
                 y_destination: float = None):

        if max_speed is None:
            max_speed = c.target_block_max_speed
        if acceleration is None:
            acceleration = c.target_block_acceleration

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=sprite_sheet,
                         max_speed=max_speed,
                         speed=(0, 0),
                         acceleration=acceleration)

        self.y_destination = y_destination

    def on_hit(self):
        return True

    def update(self):
        if self.y_destination is not None:
            self.accelerate((0, 1))
            self.move()
            if self.pos.y >= self.y_destination:
                self.pos.y = self.y_destination
                self.y_destination = None
                self.speed_y = 0.0
