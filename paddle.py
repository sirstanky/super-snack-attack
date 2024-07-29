import constants as c
import timer as t
from ball import Ball
from baseobject import BaseObject
from enum import Enum
from math import pi
from pygame import draw as pgdraw, Rect, Surface


class Paddle(BaseObject):

    def __init__(self, x, y, width, height, color, max_speed, accel, turn_accel_boost=1.0):

        self.turn_accel_boost = turn_accel_boost
        super().__init__(x, y, width, height, color, max_speed, accel)

    def accelerate(self, move_dir=''):

        if move_dir:

            move_dir = 1 if move_dir == 'e' else -1
            accel = self.accel
            travel_dir = 1 if self.speed_x > 0.0 else -1
            if self.speed_x != 0.0 and move_dir != travel_dir:
                accel *= self.turn_accel_boost
            self.speed_x += self.max_speed * accel * move_dir
            if abs(self.speed_x) > self.get_max_speed():
                self.speed_x = self.get_max_speed() * move_dir

        elif self.speed_x != 0.0:

            move_dir = 1 if self.speed_x > 0.0 else -1
            self.speed_x -= self.get_max_speed() * self.accel * move_dir
            compair = 1 if self.speed_x > 0.0 else -1
            if compair != move_dir:
                self.speed_x = 0.0

    def update(self, **kwargs):
        super().update()


class Catcher(Paddle):

    def __init__(self, color=(0, 255, 0)):

        width = c.window_width * 0.2
        height = width / 5
        x = (c.window_width / 2) - (width / 2)
        y_adjust = height / 2 + height
        y = c.window_height - y_adjust
        super().__init__(x, y, width, height, color, max_speed=2.0, accel=0.05)
        self.saved_max_speed = self.max_speed

        # Vertical drift variables
        self.drift_top = y - (height / 2)
        self.drift_bottom = y + (height / 2)
        self.drift_accel = 0.08

    def accelerate(self, move_dir=''):

        # Vertical movement
        if self.pos.y < self.drift_top:
            self.drift_accel = abs(self.drift_accel)
        elif self.pos.y > self.drift_bottom:
            self.drift_accel = abs(self.drift_accel) * -1
        self.speed_y += self.max_speed * self.drift_accel
        if abs(self.speed_y) > self.max_speed:
            self.speed_y = self.max_speed * (1 if self.drift_accel > 0.0 else -1)

        super().accelerate(move_dir)

    def get_move_direction(self, lowest_block_x: int | None):

        if lowest_block_x is not None:
            center_zone = self.pos.width / 4
            if self.pos.centerx < lowest_block_x - center_zone:
                return 'e'
            elif self.pos.centerx > lowest_block_x + center_zone:
                return 'w'

        return ''

    def update_speed(self, num_ingredients: int, weight):
        if self.max_speed > 1.0:
            self.max_speed = self.saved_max_speed - (self.saved_max_speed * (num_ingredients / weight))
            if self.max_speed < self.saved_max_speed / 10:
                self.max_speed = self.saved_max_speed / 10

    def update(self, num_ingredients: int, weight: int, lowest_block_x: int | None):
        self.update_speed(num_ingredients, weight)
        self.accelerate(self.get_move_direction(lowest_block_x))
        super().update()


class Bat(Paddle):

    def __init__(self, color=(0, 0, 255)):

        width = c.window_width * 0.2
        height = width / 4
        x = (c.window_width / 2) - (width / 2)
        y = (c.window_height / 5) * 4
        self.hit_zone: Rect = Rect(x, y - width, width, width)

        super().__init__(x, y, width, height, color, max_speed=8.0, accel=0.2)

        self.timers.add_timer(t.bat_swing_charge)
        self.timers.add_timer(t.bat_swing_cooldown)

    class Color(Enum):

        SWING = (255, 255, 255)
        CHARGED = (204, 204, 204)
        READY = (153, 153, 153)
        RECHARGING = (102, 102, 102)
        COOLDOWN = (51, 51, 51)

    def charge(self):
        if self.timers.get_time(t.bat_swing_cooldown) <= 0.0:
            self.timers.tick(t.bat_swing_charge)

    def hit_ball(self, ball: Ball):

        spread_x = (ball.pos.centerx - self.hit_zone.centerx) / (self.hit_zone.width / 2) * (pi / 4.05)
        spread_y = (abs(ball.pos.centery - self.hit_zone.y) / self.hit_zone.height) * (pi / 4.05)
        new_vector = -(pi/2) + spread_x
        new_vector += spread_y if new_vector > -(pi/2) else -spread_y
        self.timers.tick(t.bat_swing_charge)
        ball.get_hit_by_bat(new_vector, self.timers.get_time(t.bat_swing_charge))
        self.timers.reset(t.bat_swing_charge)

    def swing(self, ball: Ball):
        if self.timers.get_time(t.bat_swing_cooldown) <= 0.0:
            self.timers.set_max(t.bat_swing_cooldown)
            self.timers.reset(t.bat_swing_charge)
            if self.hit_zone.colliderect(ball.pos):
                self.hit_ball(ball)

    def update(self, **kwargs):

        self.accelerate(kwargs[c.move_direction]) if c.move_direction in kwargs else self.accelerate()
        super().update()
        self.hit_zone.topleft = self.pos.x, self.pos.y - self.pos.width

    def draw(self, window: Surface):

        cooldown = self.timers.get_time(t.bat_swing_cooldown)
        cool_max = self.timers.get_max(t.bat_swing_cooldown)
        charge = self.timers.get_time(t.bat_swing_charge)
        charge_max = self.timers.get_max(t.bat_swing_charge)

        top = Rect(self.hit_zone)
        bottom = None

        # on cooldown
        if cooldown > 0:
            top.height = top.height * self.timers.get_percent_charged(t.bat_swing_cooldown)
            bottom = Rect(self.hit_zone)
            bottom.height = self.pos.y - top.bottom - 1
            bottom.y = top.bottom + 1

            # swing
            if cooldown > cool_max * 0.9:
                top_color = self.Color.SWING.value
                bottom_color = self.Color.SWING.value

            # recharging
            else:
                top_color = self.Color.COOLDOWN.value
                bottom_color = self.Color.RECHARGING.value

        # charged up
        elif charge > 0:
            if charge == charge_max:
                top = None
                bottom = Rect(self.hit_zone)
            else:
                top.height = top.height - (top.height * self.timers.get_percent_charged(t.bat_swing_charge))
                bottom = Rect(self.hit_zone)
                bottom.height = self.pos.y - top.bottom - 1
                bottom.y = top.bottom + 1
            top_color = self.Color.READY.value
            bottom_color = self.Color.CHARGED.value

        # ready
        else:
            top_color = self.Color.READY.value
            bottom_color = self.Color.READY.value

        if top is not None:
            pgdraw.rect(window, top_color, top)
        if bottom is not None:
            pgdraw.rect(window, bottom_color, bottom)
        super().draw(window)
