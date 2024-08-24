import constants as c
from objects.paddle.paddle import Paddle
from sprites.spritesheet import SpriteSheet, get_image_and_frames

sprite_frames = [1]
sprite_sheet, frame_size = get_image_and_frames('assets/catcher.png', sprite_frames)


class Catcher(Paddle):
    def __init__(self,
                 center: tuple[float, float] = c.catcher_start_position,
                 size: tuple[float, float] = c.catcher_size,
                 max_speed: float = c.catcher_max_speed,
                 speed: tuple[float, float] = (0.0, 0.0),
                 acceleration: float = c.catcher_acceleration):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(sprite_sheet, frame_size, sprite_frames, size),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration)

        self.cur_max_speed = self.max_speed

    def draw(self):
        super().draw()
