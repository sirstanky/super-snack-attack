from pygame import Surface

from blockmanagers.fallingblockmanager import FallingBlockManager
from blockmanagers.targetmanager import TargetManager
from objects.blocks.basicblocks.targetblock import TargetBlock


class BlockManager:
    def __init__(self,
                 grid_size: tuple[int, int]):
        self.target_manager = TargetManager(grid_size)
        self.falling_manager = FallingBlockManager()

    def block_hit_by_ball(self,
                          block: TargetBlock):
        self.target_manager.remove_block(block)
        self.falling_manager.add_block(block)

    def update(self):
        self.target_manager.update()
        self.falling_manager.update()

    def draw(self,
             window: Surface):
        self.target_manager.draw(window)
        self.falling_manager.draw(window)
