import constants as c
from pygame import draw as pgdraw, Rect, Surface
from timer import TimerManager


class BaseObject:

    def __init__(self, x: float, y: float, width: float, height: float, color: tuple[int, int, int],
                 max_speed=0.0, accel=1.0, speed_x=0.0, speed_y=0.0, ):

        self.pos = Rect(x, y, width, height)
        self.color = color
        self.max_speed, self.accel = max_speed, accel
        self.speed_x, self.speed_y = speed_x, speed_y
        self.timers: TimerManager = TimerManager()

    def get_max_speed(self, total=0.0):
        total += self.max_speed
        return total

    def get_collision_direction(self, collide_obj: Rect):
        """Returns 'n', 's', 'e', or 'w' to represent which side the collision occurred on.
        Returns 'r' when the collision happens on a corner."""
        overlap_x, overlap_y = self.get_collision_overlap_ratio(collide_obj)
        # Vertical collision
        if overlap_x > overlap_y:
            return 'n' if self.pos.centery > collide_obj.centery else 's'
        # Horizontal collision
        elif overlap_x < overlap_y:
            return 'e' if self.pos.centerx < collide_obj.centerx else 'w'
        # Corner collision
        return 'r'

    def get_collision_overlap(self, collide_obj: Rect):

        overlap_x = min(self.pos.right, collide_obj.right) - max(self.pos.left, collide_obj.left)
        overlap_y = min(self.pos.bottom, collide_obj.bottom) - max(self.pos.top, collide_obj.top)
        return overlap_x, overlap_y

    def get_collision_overlap_ratio(self, collide_obj: Rect):
        """Returns the ratios of amount of overlap for horizontal and vertical sides."""

        overlap_x, overlap_y = self.get_collision_overlap(collide_obj)
        overlap_x_ratio = max(overlap_x / self.pos.width, overlap_x / collide_obj.width)
        overlap_y_ratio = max(overlap_y / self.pos.height, overlap_y / collide_obj.height)
        return overlap_x_ratio, overlap_y_ratio

    def reverse_from_collision(self, collide_obj: Rect):
        """Backs the object up on its current vector to just outside the collision."""

        overlap_x, overlap_y = self.get_collision_overlap(collide_obj)
        if overlap_x < overlap_y:
            self.pos.x -= overlap_x if self.pos.centerx < collide_obj.centerx else -overlap_x
            self.pos.y -= self.speed_y * (overlap_x / abs(self.speed_x))
        elif overlap_y < overlap_x:
            self.pos.y -= overlap_y if self.pos.centery < collide_obj.centery else -overlap_y
            self.pos.x -= self.speed_x * (overlap_y / abs(self.speed_y))
        else:
            self.pos.x -= overlap_x if self.pos.centerx < collide_obj.centerx else -overlap_x
            self.pos.y -= overlap_y if self.pos.centery < collide_obj.centery else -overlap_y

    def go(self, direction: str):
        if direction == c.up:
            self.speed_y = abs(self.speed_y) * -1
        elif direction == c.down:
            self.speed_y = abs(self.speed_y)
        elif direction == c.left:
            self.speed_x = abs(self.speed_x) * -1
        elif direction == c.right:
            self.speed_x = abs(self.speed_x)

    def move(self):
        self.pos.x += self.speed_x
        self.pos.y += self.speed_y

    def tick_timers(self, down=True, up=False):
        for timer in self.timers.timers.values():
            if down and timer.ticks_down:
                timer.tick()
            if up and not timer.ticks_down:
                timer.tick()

    def update(self, **kwargs):

        self.move()
        # Tick timers
        if 'down' in kwargs:
            if 'up' in kwargs:
                self.tick_timers(down=kwargs['down'], up=kwargs['up'])
            else:
                self.tick_timers(down=kwargs['down'])
        elif 'up' in kwargs:
            self.tick_timers(up=kwargs['up'])
        else:
            self.tick_timers()

    def draw(self, window: Surface):
        pgdraw.rect(window, self.color, self.pos)
