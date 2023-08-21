from ball import Ball
from blockmanager import TargetManager, FallingBlockManager, CaughtBlockManager
from paddle import Bat


def initialize():
    bat = Bat()
    ball = Ball(20)
    target_manager = TargetManager(4, 8)
    falling_manager = FallingBlockManager()
    caught_manager = CaughtBlockManager()

    return bat, ball, target_manager, falling_manager, caught_manager


def auto_play(bat: Bat, ball: Ball) -> str:
    bat_move = ''
    if bat.pos.centerx < ball.pos.x:
        bat_move = 'e'
    elif bat.pos.centerx > ball.pos.x + ball.pos.w:
        bat_move = 'w'

    return bat_move
