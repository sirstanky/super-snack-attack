from pygame.image import load
from pygame.transform import scale

from objects.position import Position
from sprites.sprite import Sprite


class SpriteSheet:
    def __init__(self,
                 filepath: str,
                 draw_size: tuple[float, float],
                 frame_size: tuple[int, int],
                 frames: list[int]):
        image = load(filepath).convert_alpha()
        self.image = image
        self.sprites = []
        for row, num_frames in enumerate(frames):
            sub_image = self.image.subsurface((0, frame_size[1] * row, frame_size[0] * num_frames, frame_size[1]))
            sub_image = scale(sub_image, (draw_size[0] / frame_size[0] * sub_image.get_width(),
                                          draw_size[1] / frame_size[1] * sub_image.get_height()))
            self.sprites.append(Sprite(sub_image, draw_size, num_frames))

    def draw(self,
             position: Position,
             sprite_row: int = 0,
             frame: int = None):
        self.sprites[sprite_row].draw(position, frame)
