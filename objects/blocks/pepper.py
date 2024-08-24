import constants as c
from objects.blocks.block import Block, State, get_state_speeds
from sprites.spritesheet import SpriteSheet, get_image_and_frames

sprite_frames = [1, 1, 1, 1, 1, 1]
sprite_sheet, frame_size = get_image_and_frames('assets/blocks/pepper.png', sprite_frames)


def get_pepper_speeds(state: State):
    if state == State.FALLING:
        return c.pepper_fall_speed, c.pepper_fall_acceleration
    else:
        return get_state_speeds(state)


class Pepper(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 speed: tuple[float, float] = (0.0, 0.0),
                 score_value: int = c.pepper_score,
                 target_y_dest: float = None,
                 state: State = State.TARGET):

        max_speed, acceleration = get_pepper_speeds(state)

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(sprite_sheet, frame_size, sprite_frames, size),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration,
                         score_value=score_value,
                         target_y_dest=target_y_dest,
                         state=state)

        self.hits = 3

    def change_state(self,
                     state: State):
        self.max_speed, self.acceleration = get_pepper_speeds(state)
        if state == State.TARGET:
            self.sprite.change_sprite(state.value)
        else:
            self.sprite.change_sprite(state.value + 2)
        super().change_state(state)

    def on_hit(self):
        self.hits -= 1
        self.sprite.next_sprite()
        if self.hits == 0:
            return super().on_hit()
