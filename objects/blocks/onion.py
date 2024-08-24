import constants as c
from objects.blocks.block import Block, State, get_state_speeds
from sprites.spritesheet import SpriteSheet, get_image_and_frames

sprite_frames = [1, 1, 1, 1, 1]
sprite_sheet, frame_size = get_image_and_frames('assets/blocks/onion.png', sprite_frames)


def get_onion_speeds(state: State):
    if state == State.FALLING:
        return c.onion_fall_speed, c.onion_fall_acceleration
    else:
        return get_state_speeds(state)


class Onion(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 speed: tuple[float, float] = (0.0, 0.0),
                 score_value: int = c.lettuce_score,
                 target_y_dest: float = None,
                 state: State = State.TARGET):

        max_speed, acceleration = get_onion_speeds(state)

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(sprite_sheet, frame_size, sprite_frames, size),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration,
                         score_value=score_value,
                         target_y_dest=target_y_dest,
                         state=state)

        self.sliced = False

    def change_state(self,
                     state: State):
        self.max_speed, self.acceleration = get_onion_speeds(state)
        if state == State.TARGET or state == State.FALLING:
            self.sprite.change_sprite(state.value)
        else:
            self.sprite.change_sprite(state.value + 1)
        super().change_state(state)

    def hit_by_bat(self):
        self.sliced = True
        self.sprite.next_sprite()

    def on_catch(self):
        if self.sliced:
            return super().on_catch()
