from math import pi

import pygame as pg

import constants as c
from controls.collisions import get_intersection_point
from controls.timer import Timer
from objects.ball.ball import Ball
from objects.paddle.paddle import Paddle
from objects.position import Position
from sprites.sprite import Sprite


class Bat(Paddle):
    def __init__(self,
                 center: tuple[float, float] = None,
                 size: tuple[float, float] = None,
                 color: tuple[int, int, int] = (0, 0, 255),
                 max_speed: float = None,
                 acceleration: float = None):
        if center is None:
            center = (c.window_width / 2, c.window_height * 0.75)
        if size is None:
            size = c.bat_size
        if max_speed is None:
            max_speed = c.bat_max_speed
        if acceleration is None:
            acceleration = c.bat_acceleration

        super().__init__(center,
                         size,
                         color,
                         max_speed,
                         acceleration)

        self.swing_timer = Timer(c.bat_swing_pause)
        self.player_sprite = Sprite('assets/player.png', self.pos.size, (0, 0), 2)

    @property
    def hit_zone(self):
        return Position((self.pos.x + self.pos.width / 2, self.pos.y), self.pos.size)

    def swing(self,
              ball: Ball):
        def get_closest_point():
            _closest_point = get_intersection_point((self.pos.center, ball.pos.center), ball.pos)[0]
            if _closest_point is None:
                _closest_point = (self.hit_zone.left, ball.pos.y)
            return _closest_point
            pass

        def decide_angle():
            _x_angle = (self.hit_zone.width - (ball.pos.x - self.hit_zone.left)) / self.hit_zone.width
            _y_angle = ((self.hit_zone.height / 2) - abs(ball.pos.y - self.hit_zone.y)) / (self.hit_zone.height / 2)
            scale = 1 / (_x_angle + _y_angle)
            _x_angle *= scale
            _y_angle *= scale
            if _y_angle >= 0.95:
                _x_angle = 0.0
                _y_angle = 1.0
            elif _y_angle < 0.01:
                _x_angle = 0.99
                _y_angle = 0.01
            return _x_angle, _y_angle

        if not self.swing_timer.ready:
            return
        self.speed_x, self.speed_y = 0, 0
        self.swing_timer.start()
        closest_point = get_closest_point()
        check_dist = c.get_distance(self.pos.center, closest_point)
        if self.hit_zone.collides_with_position(ball.pos) and self.hit_zone.width >= check_dist:
            x_angle, y_angle = decide_angle()
            go_right = True if ball.pos.y > self.hit_zone.y else False
            ball.hit_by_bat(x_angle, y_angle, go_right)

    def update(self,
               keys: pg.key.ScancodeWrapper):
        def check_window_boundary():
            if self.pos.x < -(self.pos.width / 5):
                self.pos.x = -(self.pos.width / 5)
                self.speed_x = 0
            elif self.pos.x + ((self.pos.width / 5) * 4) > c.window_width:
                self.pos.x = c.window_width - ((self.pos.width / 5) * 4)
                self.speed_x = 0

        def get_acceleration():
            accel = [0, 0]
            if self.swing_timer.ready:
                if keys[pg.K_UP]:
                    accel[1] -= 1
                if keys[pg.K_DOWN]:
                    accel[1] += 1
                if keys[pg.K_LEFT] and self.pos.x > -(self.pos.width / 5):
                    accel[0] -= 1
                if keys[pg.K_RIGHT] and self.pos.x + ((self.pos.width / 5) * 4) < c.window_width:
                    accel[0] += 1
            return accel[0], accel[1]

        self.swing_timer.update()
        self.accelerate(get_acceleration())
        super().update()
        check_window_boundary()
        self.hit_zone.topleft = self.pos.x, self.pos.y - self.pos.width

    def draw(self):
        pg.draw.arc(c.window, (255, 255, 255),
                    (self.pos.x - self.pos.width, self.pos.y - self.pos.width, self.pos.width * 2, self.pos.width * 2),
                    pi * 3 / 2, pi / 2, 2)
        frame = 0 if self.swing_timer.ready else 1
        self.player_sprite.draw(c.window, self.pos, frame)
