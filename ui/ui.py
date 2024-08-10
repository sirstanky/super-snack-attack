from pygame import Surface
from pygame.font import Font

import constants as c
from objects.paddle.bat import Bat
from blockmanagers.blockmanager import BlockManager


class UI:

    def __init__(self):
        self.font = Font('freesansbold.ttf', 16)

    def draw_debug_status(self,
                          bat: Bat,
                          block_manager: BlockManager,
                          window: Surface):
        bat_speed_x = self.font.render(f'Bat x speed: {bat.speed_x:.2f}', True, (255, 255, 255))
        bat_speed_y = self.font.render(f'Bat y speed: {bat.speed_y:.2f}', True, (255, 255, 255))
        speed = self.font.render(f'Target timers: {len(block_manager.drop_block_timers)}', True,
                                 (255, 255, 255))
        for index, _ in enumerate((speed, bat_speed_y, bat_speed_x)):
            text_rect = _.get_rect()
            text_rect.x = c.window_width - text_rect.width - 1
            text_rect.y = c.window_height - ((text_rect.height + (self.font.get_height() // 4)) * (index + 1))
            window.blit(_, text_rect)

    def draw_score(self,
                   block_manager: BlockManager,
                   window: Surface):
        score = self.font.render(f'Score: {len(block_manager.caught_blocks) * 10}', True, (255, 255, 255))
        rect = score.get_rect()
        rect.x, rect.y = 1, 1
        window.blit(score, rect)

    def draw(self,
             bat: Bat,
             block_manager: BlockManager,
             window: Surface):
        self.draw_debug_status(bat, block_manager, window)
        self.draw_score(block_manager, window)
