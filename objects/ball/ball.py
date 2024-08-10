from math import sqrt

from pygame.mixer import Sound

import constants as c
from objects.blocks.blockmanager import BlockManager
from controls.timer import Timer
from objects.ball.basicball import BasicBall
from objects.position import Position
from sprites.spritesheet import SpriteSheet


class Ball(BasicBall):
    def __init__(self,
                 width: float = None,
                 center: tuple[float, float] = None,
                 max_speed: float = None,
                 speed_x: float = None,
                 speed_y: float = None,
                 going_right: bool = True,
                 going_up: bool = True):

        if width is None:
            width = c.ball_width
        if center is None:
            center = (c.window_width / 2, c.window_height / 2)
        if max_speed is None:
            max_speed = c.ball_max_speed
        if speed_x is None and speed_y is None:
            speed_x = sqrt((max_speed ** 2) / 2)
            speed_y = speed_x
        else:
            if speed_x is None:
                speed_x = 0.0
            else:
                speed_y = 0.0

        sprite = SpriteSheet('assets/tomato.png', (width, width), (16, 16), [1])

        super().__init__(center=center,
                         width=width,
                         sprite_sheet=sprite,
                         max_speed=max_speed,
                         speed_x=speed_x,
                         speed_y=speed_y,
                         going_right=going_right,
                         going_up=going_up)

        self.hit_timer = Timer(0.25)
        self.hit_position = Position(self.pos.center, self.pos.size)
        self.hit_sprite = SpriteSheet('assets/ball_hit.png', (self.pos.width * 2, self.pos.height * 2), (32, 32), [1])

        self.bounce = Sound('assets/Untitled.wav')

        # DEBUG
        self.pause = False

    def hit_by_bat(self,
                   x_angle: float,
                   y_angle: float,
                   go_right: bool):
        self.hit_timer.start()
        self.hit_position.center = self.pos.center
        self.max_speed += c.ball_speed_increase_from_collisions
        self.speed_x = self.max_speed * x_angle
        self.speed_y = self.max_speed * y_angle
        self.cap_speed()
        if go_right:
            self.speed_x = abs(self.speed_x)
        else:
            self.speed_x = abs(self.speed_x) * -1
        self.speed_y = abs(self.speed_y) * -1

    def move(self,
             block_manager: BlockManager,
             distance: float = None):
        def handle_collision(shortest_dist: float,
                             closest_side: int):
            new_distance = distance - shortest_dist
            self.pos.x += self.speed_x * shortest_dist
            self.pos.y += self.speed_y * shortest_dist
            if closest_side % 2 == 1:
                self.reflect_x()
            else:
                self.reflect_y()
            # self.bounce.stop()
            # self.bounce.play()
            if new_distance > 0:
                self.move(block_manager, new_distance)

        def check_collision_with_blocks():
            closest_block = None
            closest_side = None
            shortest_dist = float('inf')
            for block in block_manager.get_all_target_blocks():
                if not self.get_bounding_box().collides_with_position(block.project_position()):
                    continue
                move_dist, collision_side = self.get_collision(block, speed_factor=distance)
                if move_dist and move_dist < shortest_dist:
                    closest_block = block
                    closest_side = collision_side
                    shortest_dist = move_dist
            if closest_block:
                block_manager.target_hit_by_ball(closest_block)
                handle_collision(shortest_dist, closest_side)
                return True

        def check_collision_with_window():
            move_dist, collision_side = self.get_collision(c.ball_boundary, speed_factor=distance, deflate=True)
            if move_dist:
                handle_collision(move_dist, collision_side)
                return True if collision_side == 2 else False
            return

        if distance is None:
            distance = 1

        if check_collision_with_blocks():
            return
        window_collision = check_collision_with_window()
        if window_collision is not None:
            return window_collision

        self.pos.x += self.speed_x * distance
        self.pos.y += self.speed_y * distance

    def update(self,
               block_manager: BlockManager):
        self.hit_timer.update()
        if not self.pause:  # TODO DEBUG (remove condition for this block)
            if self.move(block_manager):
                # TODO Return True to end the game (game over).
                # return True
                pass

    def draw(self):
        if not self.hit_timer.ready:
            self.hit_sprite.draw(self.hit_position)
        self.sprite.draw(self.pos)
