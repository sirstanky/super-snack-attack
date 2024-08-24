from math import sqrt
from time import time_ns

import pygame

from controls.states.state import State
from objects.position import Position


def time_wrapper(func):
    def inner(*args, **kwargs):
        temp_time = time_ns()
        value = func(*args, **kwargs)
        print(f"{func.__name__}: {time_ns() - temp_time}")
        return value
    return inner


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
clock = None
FPS: int = 60
game_state: list[State] | None = None

# Ball
ball_width: float = window_diagonal * 0.0272  # = 20
ball_start_position: tuple[float, float] = (window_width / 2, (window_height - top_window_ui_buffer) / 2)
ball_max_speed: float = window_diagonal * 0.0055
ball_start_speed: tuple[float, float] = (sqrt((ball_max_speed ** 2) / 2), sqrt((ball_max_speed ** 2) / 2))
ball_speed_increase_from_collisions: float = ball_max_speed * 0.0125
ball_window_boundary: Position = Position(
    (window_width / 2, (window_height - top_window_ui_buffer) / 2 + top_window_ui_buffer),
    (window_width, window_height - top_window_ui_buffer))

# Bat
bat_start_position: tuple[float, float] = (window_width / 2, window_height * 0.75)
_bat_width: float = window_diagonal * 0.0735
bat_size: tuple[float, float] = (_bat_width, _bat_width * 2)
bat_max_speed: float = window_width * 0.017  # = 6.0
bat_acceleration: float = window_width * 0.0006  # = 0.1
bat_swing_pause: float = 0.5  # in seconds

# Catcher
catcher_start_position: tuple[float, float] = (window_width / 2, window_height * 0.95)
catcher_size: tuple[float, float] = (window_width * 0.15, window_width * 0.03)
catcher_max_speed: float = window_width * 0.0085
catcher_acceleration: float = window_width * 0.00007

# Block manager
target_columns: int = 15
target_rows: int = 6
target_area: int = int(window_height * 0.15)
target_block_drop_delay: float = 7.0

# Blocks
block_size: tuple[float, float] = ((window_width / target_columns) - (window_width / target_columns) / 10,
                                   ((target_area + top_window_ui_buffer) / target_rows) - (
                                               window_width / target_columns) / 10)

target_block_max_speed: float = window_height * 0.00625
target_block_acceleration: float = window_height * 0.000156

cheese_fall_speed: float = target_block_max_speed
cheese_fall_acceleration: float = target_block_acceleration
cheese_score: int = 10

lettuce_fall_speed: float = 1.5
lettuce_fall_acceleration: float = target_block_acceleration / 10
lettuce_swing_distance: float = window_width / 8
lettuce_drop_distance: float = window_height / 10
lettuce_score: int = 20

onion_fall_speed: float = target_block_max_speed
onion_fall_acceleration: float = target_block_acceleration
onion_score: int = 30

pepper_fall_speed: float = target_block_max_speed
pepper_fall_acceleration: float = target_block_acceleration
pepper_score: int = 40

pickle_fall_speed: float = target_block_max_speed
pickle_fall_acceleration: float = target_block_acceleration
pickle_score = 50

sock_fall_speed: float = target_block_max_speed
sock_fall_acceleration: float = target_block_acceleration

caught_block_size: tuple[float, float] = (catcher_size[0] * 1.1, max(catcher_size[1] / 4, 1))
