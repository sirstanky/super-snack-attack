from pygame import Surface

import constants as c
from objects.position import Position


class Sprite:
    def __init__(self,
                 image: Surface,
                 draw_size: tuple[float, float],
                 num_frames: int = 1):
        self.image = image
        self.draw_size = draw_size
        self.num_frames = num_frames
        self.cur_frame = 0
        self.frame_tick = 0

    def advance_frame(self):
        self.cur_frame += 1
        if self.cur_frame >= self.num_frames:
            self.cur_frame = 0

    def set_frame(self,
                  frame: int):
        self.cur_frame = frame
        if self.cur_frame >= self.num_frames:
            raise Exception("Frame set to sprite is higher than the number of frames the sprite contains.")

    def reset(self):
        self.cur_frame = 0

    def draw(self,
             position: Position,
             frame: int = None):
        if frame is None:
            frame = self.cur_frame
            self.frame_tick += 1
            if self.frame_tick > 8:
                self.advance_frame()
        image = self.image.subsurface((self.draw_size[0] * frame, 0, self.draw_size[0], self.draw_size[1]))
        c.window.blit(image, (position.left, position.top))
