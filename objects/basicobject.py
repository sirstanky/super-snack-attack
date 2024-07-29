from math import sqrt

from pygame import draw as pgdraw, Surface

import constants as c
from objects.position import Position


class BasicObject:
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 color: tuple[int, int, int],
                 max_speed: float,
                 speed: tuple[float, float] = None,
                 acceleration: float = 1.0):
        if speed is None:
            speed = (0.0, 0.0)
        if c.get_distance(speed[0], speed[1]) > max_speed:
            raise Exception("Speed set higher than max speed.")

        self._pos = Position(center, size)
        # TODO Eventually we will phase out 'color' for sprites.
        self.color = color
        self._max_speed = max_speed
        self._speed = list(speed)
        self._acceleration = acceleration

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self,
            new_center: tuple[float, float]):
        self._pos.center = new_center

    @property
    def speed(self):
        return self._speed

    @property
    def speed_x(self):
        return self._speed[0]

    @speed_x.setter
    def speed_x(self,
                new_x_speed: float):
        self._speed[0] = new_x_speed

    @property
    def speed_y(self):
        return self._speed[1]

    @speed_y.setter
    def speed_y(self,
                new_y_speed: float):
        self._speed[1] = new_y_speed

    @property
    def max_speed(self):
        return self._max_speed

    @max_speed.setter
    def max_speed(self,
                  new_max_speed: float):
        self._max_speed = new_max_speed

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self,
                     new_acceleration: float):
        self._acceleration = new_acceleration

    def project_position(self,
                         speed_factor: float = 1.0):
        new_pos = self.pos.x + (self.speed_x * speed_factor), self.pos.y + (self.speed_y * speed_factor)
        return Position(new_pos, self.pos.size)

    def get_other_vector(self,
                         vector: float):
        if vector > self.max_speed:
            raise Exception("Vector length cannot exceed max speed.")
        return sqrt(self.max_speed ** 2 - vector ** 2)

    def cap_speed(self):
        speed = c.get_distance(self.speed_x, self.speed_y)
        if speed > self.max_speed:
            if abs(self.speed_x) < abs(self.speed_y):
                self.speed_y = self.get_other_vector(self.speed_x) * (1 if self.speed_y > 0 else -1)
            else:
                self.speed_x = self.get_other_vector(self.speed_y) * (1 if self.speed_x > 0 else -1)
            new_speed = c.get_distance(self.speed_x, self.speed_y)
            if new_speed > self.max_speed:
                scale = self.max_speed / new_speed
                self.speed_x *= scale
                self.speed_y *= scale

    def get_bounding_box(self):
        new_pos = self.project_position()
        x1, y1 = min(self.pos.left, new_pos.left), min(self.pos.top, new_pos.top)
        x2, y2 = max(self.pos.right, new_pos.right), max(self.pos.bottom, new_pos.bottom)
        center = (x1 + x2) / 2, (y1 + y2) / 2
        size = x2 - x1, y2 - y1
        return Position(center, size)

    def reflect_x(self):
        self.speed_x = -self.speed_x

    def reflect_y(self):
        self.speed_y = -self.speed_y

    def accelerate(self,
                   acceleration: tuple[int, int]):
        def decelerate(start_speed: float):
            friction = 1.0 - self.acceleration
            if -(self.acceleration / 3) <= start_speed <= (self.acceleration / 3):
                return 0
            else:
                return start_speed * friction

        def accel_val(start_speed: float,
                      accel: int):
            return accel * 2 if min(start_speed, accel) < 0 < max(start_speed, accel) else accel

        self.speed_x += accel_val(self.speed_x, acceleration[0]) * self.acceleration
        self.speed_y += accel_val(self.speed_y, acceleration[1]) * self.acceleration
        if acceleration[0] == 0:
            self.speed_x = decelerate(self.speed_x)
        if acceleration[1] == 0:
            self.speed_y = decelerate(self.speed_y)
        self.cap_speed()

    def move(self,
             *args):
        self.pos.x += self.speed_x
        self.pos.y += self.speed_y
        self.pos.center = (self.pos.x, self.pos.y)

    def update(self,
               *args):
        self.move()

    def draw(self, window: Surface):
        pgdraw.rect(window, self.color, self.pos.draw_rect)
