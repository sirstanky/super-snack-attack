import constants as c

from objects.blocks.block import Block, State, get_state_speeds
from sprites.spritesheet import SpriteSheet, get_image_and_frames

sprite_frames = [1, 1, 1, 1]
sprite_sheet, frame_size = get_image_and_frames('assets/blocks/cheese.png', sprite_frames)


def get_cheese_speeds(state: State):
    if state == State.FALLING:
        return c.cheese_fall_speed, c.cheese_fall_acceleration
    else:
        return get_state_speeds(state)


class Cheese(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 speed: tuple[float, float] = (0.0, 0.0),
                 score_value: int = c.cheese_score,
                 target_y_dest: float = None,
                 state: State = State.TARGET):

        max_speed, acceleration = get_cheese_speeds(state)

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(sprite_sheet, frame_size, sprite_frames, size),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration,
                         score_value=score_value,
                         target_y_dest=target_y_dest,
                         state=state)

    def change_state(self,
                     state: State):
        self.max_speed, self.acceleration = get_cheese_speeds(state)
        self.sprite.change_sprite(state.value)
        super().change_state(state)
