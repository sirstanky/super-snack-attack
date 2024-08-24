from math import pi

import pygame as pg

import constants as c
from controls.timer import Timer
from objects.ball.ball import Ball
from objects.blocks.block import Block
from objects.paddle.paddle import Paddle
from objects.position import Position
from sprites.spritesheet import SpriteSheet, get_image_and_frames

sprite_frames = [2]
sprite_sheet, frame_size = get_image_and_frames('assets/player.png', sprite_frames)


class Bat(Paddle):
    def __init__(self,
                 center: tuple[float, float] = c.bat_start_position,
                 size: tuple[float, float] = c.bat_size,
                 max_speed: float = c.bat_max_speed,
                 speed: tuple[float, float] = (0.0, 0.0),
                 acceleration: float = c.bat_acceleration):

        super().__init__(center=center,
                         size=size,
                         sprite_sheet=SpriteSheet(sprite_sheet, frame_size, sprite_frames, size),
                         max_speed=max_speed,
                         speed=speed,
                         acceleration=acceleration)

        self.swing_timer = Timer(c.bat_swing_pause)

    @property
    def hit_zone(self):
        return Position((self.pos.x + self.pos.width / 2, self.pos.y), self.pos.size)

    def swing(self,
              ball: Ball,
              falling_blocks: list[Block]):

        def get_closest_point():
            def get_intersection_point():
                def line_intersects_line():
                    def point_on_line(_line: tuple[tuple[float, float], tuple[float, float]]):
                        px, py = round(point[0], 3), round(point[1], 3)
                        (_x1, _y1), (_x2, _y2) = (round(_line[0][0], 3), round(_line[0][1], 3)), (
                            round(_line[1][0], 3), round(_line[1][1], 3))
                        return min(_x1, _x2) <= px <= max(_x1, _x2) and min(_y1, _y2) <= py <= max(_y1, _y2)

                    (x1, y1), (x2, y2) = line
                    (x3, y3), (x4, y4) = edge
                    base = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                    if base == 0:
                        return None
                    intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / base
                    intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / base
                    point = (intersect_x, intersect_y)
                    if point_on_line(line) and point_on_line(edge):
                        return intersect_x, intersect_y

                line = (self.pos.center, ball.pos.center)
                rect = ball.pos
                edges = [rect.top_edge, rect.right_edge, rect.bottom_edge, rect.left_edge]
                shortest_distance = float('inf')
                closest_intersection = None
                for direction, edge in enumerate(edges):
                    intersection = line_intersects_line()
                    if intersection:
                        new_distance = c.get_distance(line[0], intersection)
                        if new_distance < shortest_distance:
                            shortest_distance = new_distance
                            closest_intersection = intersection
                return closest_intersection

            _closest_point = get_intersection_point()
            if _closest_point is None:
                _closest_point = (self.hit_zone.left, ball.pos.y)
            return _closest_point

        def decide_angle():
            # TODO Remove x_angle, no longer needed
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

        for block in falling_blocks:
            if self.hit_zone.collides_with_position(block.pos):
                block.hit_by_bat()

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
                if keys[pg.K_LEFT]:
                    accel[0] -= 1
                if keys[pg.K_RIGHT]:
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
        self.sprite.draw(self.pos, frame)
