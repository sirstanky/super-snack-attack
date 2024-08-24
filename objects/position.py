from __future__ import annotations


class Position:
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float]):
        self._x, self._y = center
        self._width, self._height = size

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self,
              new_width: float):
        self._width = new_width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self,
               new_height: float):
        self._height = new_height

    @property
    def size(self):
        return self._width, self._height

    @size.setter
    def size(self,
             new_size: tuple[float, float]):
        self._width, self._height = new_size

    @property
    def center(self):
        return self._x, self._y

    @center.setter
    def center(self,
               new_center: tuple[float, float]):
        self._x, self._y = new_center

    @property
    def left(self):
        return self._x - self._width / 2

    @left.setter
    def left(self,
             new_left: float):
        self._x = new_left + self._width / 2

    @property
    def right(self):
        return self._x + self._width / 2

    @right.setter
    def right(self,
              new_right: float):
        self._x = new_right - self._width / 2

    @property
    def top(self):
        return self._y - self._height / 2

    @top.setter
    def top(self,
            new_top: float):
        self._y = new_top + self._height / 2

    @property
    def bottom(self):
        return self._y + self._height / 2

    @bottom.setter
    def bottom(self,
               new_bottom: float):
        self._y = new_bottom - self._height / 2

    @property
    def top_left(self):
        return self.left, self.top

    @top_left.setter
    def top_left(self,
                 new_top_left: tuple[float, float]):
        self.left, self.top = new_top_left

    @property
    def top_right(self):
        return self.right, self.top

    @top_right.setter
    def top_right(self,
                  new_top_right: tuple[float, float]):
        self.right, self.top = new_top_right

    @property
    def bottom_left(self):
        return self.left, self.bottom

    @bottom_left.setter
    def bottom_left(self,
                    new_bottom_left: tuple[float, float]):
        self.left, self.bottom = new_bottom_left

    @property
    def bottom_right(self):
        return self.right, self.bottom

    @bottom_right.setter
    def bottom_right(self,
                     new_bottom_right: tuple[float, float]):
        self.right, self.bottom = new_bottom_right

    @property
    def mid_left(self):
        return self.left, self._y

    @property
    def mid_right(self):
        return self.right, self._y

    @property
    def mid_top(self):
        return self._x, self.top

    @property
    def mid_bottom(self):
        return self._x, self.bottom

    @property
    def top_edge(self):
        return self.top_left, self.top_right

    @property
    def bottom_edge(self):
        return self.bottom_left, self.bottom_right

    @property
    def left_edge(self):
        return self.top_left, self.bottom_left

    @property
    def right_edge(self):
        return self.top_right, self.bottom_right

    @property
    def draw_rect(self):
        return self.top_left, self.size

    def inflate(self,
                size: tuple[float, float]):
        return Position(self.center, (self.width + size[0], self.height + size[1]))

    def deflate(self,
                size: tuple[float, float]):
        return Position(self.center, (self.width - size[0], self.height - size[1]))

    def collides_with_position(self,
                               check_pos: Position):
        vert, hor = False, False
        if check_pos.left <= self.left <= check_pos.right or check_pos.left <= self.right <= check_pos.right:
            vert = True
        elif self.left <= check_pos.left <= self.right or self.left <= check_pos.right <= self.right:
            vert = True
        if check_pos.top <= self.top <= check_pos.bottom or check_pos.top <= self.bottom <= check_pos.bottom:
            hor = True
        elif self.top <= check_pos.top <= self.bottom or self.top <= check_pos.bottom <= self.bottom:
            hor = True
        return vert and hor

    def collides_with_point(self,
                            point: tuple[float, float]):
        return self.left <= point[0] <= self.right and self.top <= point[1] <= self.bottom
