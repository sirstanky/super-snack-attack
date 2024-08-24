from pygame import Surface
from pygame.image import load
from pygame.transform import scale

from objects.position import Position
from sprites.sprite import Sprite


def get_image_and_frames(filepath: str,
                         row_frames: list[int]):
    image = load(filepath).convert_alpha()
    frame_width = image.get_width() // max(row_frames)
    frame_height = image.get_height() // len(row_frames)
    return image, (frame_width, frame_height)


class SpriteSheet:
    def __init__(self,
                 sprite_sheet: Surface,
                 frame_size: tuple[int, int],
                 frame_list: list[int],
                 draw_size: tuple[float, float]):
        self.sprites = []
        for row, num_frames in enumerate(frame_list):
            sub_image = sprite_sheet.subsurface((0, frame_size[1] * row, frame_size[0] * num_frames, frame_size[1]))
            sub_image = scale(sub_image, (draw_size[0] / frame_size[0] * sub_image.get_width(),
                                          draw_size[1] / frame_size[1] * sub_image.get_height()))
            self.sprites.append(Sprite(sub_image, draw_size, num_frames))
        self.current_sprite = self.sprites[0]

    def change_sprite(self,
                      new_sprite_row: int):
        self.current_sprite = self.sprites[new_sprite_row]

    def next_sprite(self):
        self.current_sprite = self.sprites[self.sprites.index(self.current_sprite) + 1]

    def draw(self,
             position: Position,
             frame: int = None):
        self.current_sprite.draw(position, frame)
