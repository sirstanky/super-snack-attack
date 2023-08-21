import constants as c
import timer as t
from blockmanager import BlockManager
from game import initialize
import math as m
import pygame as pg


# Initialize pygame
pg.init()

# Set up the game window
window = pg.display.set_mode((c.window_width, c.window_height))
pg.display.set_caption("Super Snack Attack")

# Set up game variables
clock = pg.time.Clock()
FPS = 60

# Game objects
bat, ball, target_manager, falling_manager, caught_manager = initialize()

# Debug display font
font = pg.font.Font('freesansbold.ttf', 16)

# Game loop
running = True
auto_play = False
keys = pg.key.get_pressed()
while running:

    for event in pg.event.get():
        # Quit control
        if event.type == pg.QUIT:
            running = False
            continue
        # DEBUG click events
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()

            # Click on sandwich to halve the number of caught ingredients
            if caught_manager.blocks:
                w = caught_manager.blocks[0].pos.width
                h = caught_manager.blocks[0].pos.height * len(caught_manager.blocks)
                x, y = caught_manager.blocks[-1].pos.topleft
                sandwich = pg.Rect(x, y, w, h)
                if sandwich.collidepoint(mouse_pos[0], mouse_pos[1]):
                    while len(caught_manager.blocks) > caught_manager.catch_limit / 2:
                        caught_manager.blocks.pop(-1)

            # Click target blocks to make them fall
            for row in target_manager.blocks:
                for block in row[0].blocks:
                    if block.pos.collidepoint(mouse_pos[0], mouse_pos[1]):
                        falling_manager.add_block(block)
                        if target_manager.remove_block(block):
                            target_manager.new_rows_queue.append([BlockManager(target_manager.make_new_row(0)), row[1]])

    prev_keys = keys
    keys = pg.key.get_pressed()

    # DEBUG pause ball
    if keys[pg.K_UP] and not prev_keys[pg.K_UP]:
        ball.pause = True if not ball.pause else False

    # Move bat
    bat_move = ''
    if not keys[pg.K_SPACE] and prev_keys[pg.K_SPACE]:
        bat.swing(ball)
    elif keys[pg.K_SPACE]:
        bat.charge()
    if keys[pg.K_LEFT] and bat.pos.x > 0:
        bat_move = 'w'
    elif keys[pg.K_RIGHT] and bat.pos.x + bat.pos.w < c.window_width:
        bat_move = 'e'

    # Update objects
    # TODO bat update should handle all actions that could be sent to it. that's why we're using kwargs
    bat.update(move_direction=bat_move)
    # Ball update returns if it has hit the bottom of the window
    # TODO this is a gross way to check game over. Figure something else out.
    game_over = ball.update()
    if game_over is not None:
        bat, catcher, ball, block_manager = initialize()
        continue
    target_manager.update(ball, falling_manager)
    falling_manager.update()
    caught_manager.update(falling_manager)

    # Draw game objects
    window.fill((0, 0, 0))
    caught_manager.draw(window)
    target_manager.draw(window)
    falling_manager.draw(window)
    bat.draw(window)
    ball.draw(window)

    # Text block
    buffer = font.get_height() // 4
    ball_x = font.render(f'Ball x speed: {ball.speed_x:.2f}', True, (255, 255, 255))
    ball_y = font.render(f'Ball y speed: {ball.speed_y:.2f}', True, (255, 255, 255))
    ball_speed = font.render(f'Ball speed: {m.sqrt(ball.speed_x**2 + ball.speed_y**2):.2f}', True, (255, 255, 255))
    ball_max_speed = ball.get_max_speed() + ball.timers.get_time(t.ball_stored_speed_increase)
    ball_max_speed = font.render(f'Ball max speed: {ball_max_speed:.2f}', True, (255, 255, 255))
    for index, _ in enumerate((ball_max_speed, ball_speed, ball_y, ball_x)):
        text_rect = _.get_rect()
        text_rect.x = c.window_width - text_rect.width - 1
        text_rect.y = c.window_height - ((text_rect.height + buffer) * (index + 1))
        window.blit(_, text_rect)

    pg.display.update()
    clock.tick(FPS)

# Quit the game
pg.quit()
