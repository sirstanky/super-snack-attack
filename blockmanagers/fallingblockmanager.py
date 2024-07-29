from random import random

import constants as c
from blockmanagers.basicblockmanager import BasicBlockManager
from objects.blocks.basicblocks.basicblock import BasicBlock
from objects.blocks.basicblocks.fallingblock import FallingBlock
from objects.blocks.floatingblock import FloatingBlock


class FallingBlockManager(BasicBlockManager):
    def __init__(self,
                 blocks: list[FallingBlock] = None):
        super().__init__(blocks=blocks)

    def add_block(self,
                  block: BasicBlock,
                  index: int = None):
        if random() < 0.5:
            new_block = FallingBlock(block.pos.center, block.pos.size, block.color, speed=block.speed)
        else:
            new_block = FloatingBlock(block.pos.center, block.pos.size, block.color)
        super().add_block(new_block)

    def get_lowest_block(self,
                         limit: int):
        lowest_block = None
        lowest_y = 0
        for block in self.get_blocks():
            if lowest_y < block.pos.bottom < limit:
                lowest_y = block.pos.bottom
                lowest_block = block
        return lowest_block

    def update(self):
        for block in self.get_blocks():
            block.update()
            if block.pos.top > c.window_height:
                self.remove_block(block)
