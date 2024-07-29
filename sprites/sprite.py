from pygame import Surface
from pygame.image import load
from pygame.transform import scale

from objects.position import Position


class Sprite:
    def __init__(self,
                 filepath: str,
                 draw_size: tuple[float, float],
                 draw_offset: tuple[float, float] = (0.0, 0.0),
                 num_frames: int = 1):
        image = load(filepath).convert_alpha()
        image = scale(image, (draw_size[0] * num_frames, draw_size[1]))
        self.image = image
        self.size = (image.get_width() / num_frames, image.get_height())
        self.draw_offset = draw_offset
        self.num_frames = num_frames

    def draw(self,
             window: Surface,
             position: Position,
             frame: int = 0):
        if frame >= self.num_frames:
            raise Exception("Given frame number exceeds frames for this sprite.")
        image = self.image.subsurface((self.size[0] * frame, 0, self.size[0], self.size[1]))
        window.blit(image, (position.left + self.draw_offset[0], position.top + self.draw_offset[1]))
