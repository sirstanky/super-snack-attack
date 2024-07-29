from pygame import Surface

import constants as c
from blockmanagers.basicblockmanager import BasicBlockManager
from objects.blocks.basicblocks.caughtblock import CaughtBlock


class CaughtBlockManager(BasicBlockManager):
    def __init__(self,
                 blocks: list[CaughtBlock] = None):
        self.display_limit = c.caught_blocks_display_limit
        super().__init__(blocks=blocks)

    def update(self,
               position: tuple[float, float]):

        for block in self.get_blocks():
            block.update(position)

    def draw(self,
             window: Surface):
        for block in self.get_blocks()[:self.display_limit]:
            block.draw(window)
