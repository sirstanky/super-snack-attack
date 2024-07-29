from math import sqrt

import pygame

from objects.position import Position


def get_distance(start: tuple[float, float] | float,
                 end: tuple[float, float] | float):
    try:
        x1, y1 = start
    except TypeError:
        x1, y1 = 0, 0
    try:
        x2, y2 = end
    except TypeError:
        x2, y2 = start, end
    return sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


# Window
window: pygame.Surface | None = None
window_width: int = 360
window_height: int = window_width // 9 * 16
window_diagonal: float = get_distance(window_width, window_height)  # 734.4 @ width of 360
top_window_ui_buffer = window_height * 0.056

# Game
clock: pygame.time.Clock | None = None
FPS = 60

# Ball
ball_max_speed: float = window_diagonal * 0.0055
ball_speed_increase_from_collisions: float = ball_max_speed * 0.0125
ball_width: float = window_diagonal * 0.0272  # = 20
boundary_center = (window_width / 2, (window_height - top_window_ui_buffer) / 2 + top_window_ui_buffer)
boundary_size = window_width, window_height - top_window_ui_buffer
ball_boundary: Position = Position(boundary_center, boundary_size)

# Bat
bat_width: float = window_width * 0.15
bat_size: tuple[float, float] = (bat_width, bat_width * 2)
bat_max_speed: float = window_width * 0.017  # = 6.0
bat_acceleration: float = window_width * 0.0006  # = 0.1
bat_swing_pause: float = 0.5  # in seconds

# Catcher
catcher_size: tuple[float, float] = (window_width * 0.15, window_width * 0.03)
catcher_max_speed: float = window_width * 0.0085
catcher_acceleration: float = window_width * 0.00007

# Blocks
falling_block_speed: float = window_height * 0.00625  # = 4
falling_block_acceleration: float = window_height * 0.000156
target_block_speed: float = falling_block_speed
target_block_acceleration: float = falling_block_acceleration
caught_block_size: tuple[float, float] = (catcher_size[0] * 1.1, max(catcher_size[1] / 4, 1))
floating_block_swing_distance: float = window_width / 8
floating_block_drop_distance: float = window_height
floating_block_speed: float = 1

# Block managers
caught_blocks_display_limit: int = 20
target_manager_drop_delay: float = 7.0
queue_manager_new_blocks_delay: float = 12.0  # in seconds
target_columns: int = 10
target_rows: int = 4
target_area: int = int(window_height * 0.15)
