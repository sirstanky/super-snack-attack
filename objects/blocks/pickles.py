import constants as c
from objects.blocks.block import Block, State, get_state_speeds
from sprites.spritesheet import SpriteSheet, get_image_and_frames

sprite_frames = [1, 1, 1, 1]
sprite_sheet, frame_size = get_image_and_frames('assets/blocks/pickle.png', sprite_frames)


def get_pickle_speed(state: State):
    if state == State.FALLING:
        return c.pickle_fall_speed, c.pickle_fall_acceleration
    else:
        return get_state_speeds(state)


class Pickle(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 speed: tuple[float, float] = (0.0, 0.0),
                 score_value: int = c.pickle_score,
                 target_y_dest: float = None,
                 state: State = State.TARGET):

        max_speed, acceleration = get_pickle_speed(state)

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(sprite_sheet, frame_size, sprite_frames, size),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration,
                         score_value=score_value,
                         target_y_dest=target_y_dest,
                         state=state)

        if state == State.FALLING:
            self.set_knock_speed()
            self.sprite.change_sprite(state.value)

    def change_state(self,
                     state: State):
        self.max_speed, self.acceleration = get_pickle_speed(state)
        self.sprite.change_sprite(state.value)
        super().change_state(state)

    def on_hit(self):
        super().on_hit()
        self.set_knock_speed()
        return True

    def update(self,
               catcher_position: tuple[float, float],
               stack_layer: int):
        if self.state == State.FALLING:
            self.fall_at_angle()
        else:
            super().update(catcher_position, stack_layer)
