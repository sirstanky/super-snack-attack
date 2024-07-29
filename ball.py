import constants as c
import timer as t
from baseobject import BaseObject
from math import cos, sin, sqrt
from pygame import draw as pgdraw, Rect, Surface


class Ball(BaseObject):

    def __init__(self, width: int, color=(255, 255, 255), max_speed=c.ball_max_speed):

        x = (c.window_width - width) / 2
        y = (c.window_height - width) / 2
        speed = sqrt(max_speed**2 / 2)

        super().__init__(x, y, width, width, color, max_speed=max_speed, speed_x=speed, speed_y=speed)

        self.radius = width / 2
        self.speed_increase_from_collision = c.ball_speed_increase_from_collisions
        self.timers.add_timer(t.ball_stored_speed_increase)
        self.timers.add_timer(t.ball_temporary_speed_increase)

        # DEBUG
        self.pause = False

    def get_max_speed(self, total=0.0):
        """Returns max speed plus all speed bonuses."""
        total += self.timers.get_time(t.ball_temporary_speed_increase)
        return super().get_max_speed(total)

    def get_speed_vector(self):
        """Returns the x and y vector ratios."""
        total_speed = sqrt(self.speed_x**2 + self.speed_y**2)
        speed_x_ratio, speed_y_ratio = self.speed_x / total_speed, self.speed_y / total_speed
        return speed_x_ratio, speed_y_ratio

    def set_speed_vector(self, new_vector: float):
        """Sets x and y speed and direction from radians."""
        self.speed_x = self.get_max_speed() * cos(new_vector)
        self.speed_y = self.get_max_speed() * sin(new_vector)

    def get_hit_by_bat(self, new_vector: float, boost: float):
        """Adjust speed and direction after getting hit by the bat."""
        self.max_speed += self.timers.get_time(t.ball_stored_speed_increase)
        self.timers.reset(t.ball_stored_speed_increase)
        self.set_speed_vector(new_vector)
        self.timers.adjust_time(t.ball_temporary_speed_increase, boost)

    def simple_collision(self, collide_obj: Rect):
        """Changes the ball's direction after a collision and reverses its position to the collision's edge."""
        collide_dir = self.get_collision_direction(collide_obj)
        match collide_dir:
            case 'n':
                self.speed_y = abs(self.speed_y)
            case 's':
                self.speed_y = abs(self.speed_y) * -1
            case 'e':
                self.speed_x = abs(self.speed_x) * -1
            case 'w':
                self.speed_x = abs(self.speed_x)
            case 'r':
                if self.pos.centerx < collide_obj.centerx:
                    self.speed_x = abs(self.speed_x) * -1
                else:
                    self.speed_x = abs(self.speed_x)
                if self.pos.centery < collide_obj.centery:
                    self.speed_y = abs(self.speed_y) * -1
                else:
                    self.speed_y = abs(self.speed_y)
        self.reverse_from_collision(collide_obj)

    def update(self):
        """Sets the current speed and checks for collision with walls."""

        def update_speed():
            x_ratio, y_ratio = self.get_speed_vector()
            self.speed_x = self.get_max_speed() * x_ratio
            self.speed_y = self.get_max_speed() * y_ratio

        def check_collision_with_walls():
            # TODO this needs to handle collisions with the bottom differently. Eventually.
            collide_x, collide_y = '', ''
            if self.pos.x < 0:
                collide_x = c.left
            elif self.pos.right > c.window_width:
                collide_x = c.right
            if self.pos.y < 0:
                collide_y = c.top
            elif self.pos.bottom > c.window_height:
                collide_y = c.bottom
            if collide_x or collide_y:
                self.timers.adjust_time(t.ball_stored_speed_increase, self.speed_increase_from_collision)
                self.pos.x -= self.speed_x
                self.pos.y -= self.speed_y
                if collide_x:
                    if collide_x == c.left:
                        dist_x = self.pos.left
                        self.pos.left = 0
                        self.go(c.right)
                    else:
                        dist_x = self.pos.right - c.window_width + 1
                        self.pos.right = c.window_width - 1
                        self.go(c.left)
                    ratio = dist_x / abs(self.speed_x)
                    dist_y = self.speed_y * ratio
                    self.pos.y += dist_y
                else:
                    if collide_y == c.top:
                        dist_y = abs(self.pos.top)
                        self.pos.top = 0
                        self.go(c.down)
                    else:
                        dist_y = self.pos.bottom - c.window_height + 1
                        self.pos.bottom = c.window_height - 1
                        self.go(c.up)
                    ratio = dist_y / abs(self.speed_y)
                    dist_x = self.speed_x * ratio
                    self.pos.x += dist_x
                dist_x = self.speed_x - dist_x
                dist_y = self.speed_y - dist_y
                self.pos.x += dist_x
                self.pos.y += dist_y
                check_collision_with_walls()

        if not self.pause:  # DEBUG (remove condition for this block)
            update_speed()
            super().update(down=True, up=True)
            check_collision_with_walls()

    def draw(self, window: Surface):
        pgdraw.circle(window, self.color, self.pos.center, self.radius, self.pos.w)
