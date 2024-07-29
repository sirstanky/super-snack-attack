from ball import Ball
from baseobject import BaseObject
from random import randint


class Block(BaseObject):

    def __init__(self, x: float, y: float, width: float, height: float, color: tuple[int, int, int], max_speed=0.0):
        super().__init__(x, y, width, height, color, max_speed=max_speed)


class TargetBlock(Block):

    def __init__(self, row: int, column: int, width: float, height: float, gap: float, color=(0, 0, 255)):
        self.column = column
        self.row = row
        x = (width + gap) * column + (gap / 2)
        y = (height + gap) * row + gap
        super().__init__(x, y, width, height, color)

    def update(self, ball: Ball):
        if self.pos.colliderect(ball.pos):
            ball.simple_collision(self.pos)
            return True


class CaughtBlock(Block):

    def __init__(self, catcher_pos: tuple[int, int], stack_height: int, width: float, height: float,
                 color=(randint(0, 255), randint(0, 255), randint(0, 255))):
        x = catcher_pos[0] - (width / 2)
        self.x_offset = catcher_pos[0] - x
        y = catcher_pos[1] - (stack_height * height)
        super().__init__(x, y, width, height, color)

    def update(self, catcher_pos: tuple[int, int], index):
        self.pos.x = catcher_pos[0] - self.x_offset
        self.pos.y = catcher_pos[1] - (self.pos.height * (index + 1))
