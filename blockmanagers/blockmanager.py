from random import random

import constants as c
from blockmanagers.fallingblockmanager import FallingBlockManager
from blockmanagers.targetmanager import TargetManager
from objects.blocks.basicblocks.targetblock import TargetBlock
from objects.blocks.basicblocks.block import Block
from objects.blocks.cheese import Cheese
from objects.blocks.lettuce import Lettuce
from controls.timer import Timer

block_table = [
    (0.5, Cheese),
    (1.0, Lettuce)
]


class BlockManager:
    def __init__(self,
                 grid_size: tuple[int, int]):
        def find_block_size():
            column_width = c.window_width / self.target_columns
            gap = column_width / 10
            block_width = column_width - gap
            block_height = ((c.target_area + c.top_window_ui_buffer) / self.target_rows) - gap
            return block_width, block_height

        def find_target_and_drop_positions():
            block_width, block_height = self.block_size
            gap = (c.window_width / self.target_columns) / 10
            x = [int(((block_width + gap) * _ + (gap // 2)) + (block_width // 2))
                 for _ in range(self.target_columns)]
            y = [int(((block_height + gap) * _ + gap) + (block_height // 2) + c.top_window_ui_buffer)
                 for _ in range(self.target_rows)]
            target_positions = [[(x[i], y[j]) for j in range(self.target_rows)] for i in range(self.target_columns)]
            drop_positions = [[(x[i], y[j]) for j in range(self.target_rows)] for i in range(self.target_columns)]
            for x in range(len(drop_positions)):
                for y in range(len(drop_positions[x])):
                    drop_positions[x][y] = drop_positions[x][y][0], -drop_positions[x][y][1]
                drop_positions[x].reverse()
            return target_positions, drop_positions

        self.target_columns = grid_size[0]
        self.target_rows = grid_size[1]
        self.block_size = find_block_size()
        self.target_positions, self.drop_positions = find_target_and_drop_positions()
        self.drop_block_timers: dict[Timer, int] = {}
        self.target_blocks: list[list[Block]] = [[Cheese(self.target_positions[x][y], self.block_size)
                                                 for y in range(self.target_rows)]
                                                 for x in range(self.target_columns)]
        self.falling_blocks: list[Block] = []
        self.caught_blocks: list[Block] = []

    def get_all_target_blocks(self):
        target_blocks = []
        for column in self.target_blocks:
            target_blocks += [block for block in column if block is not None]
        return target_blocks

    def get_target_block_coordinate(self,
                                    target_block: Block):
        for x, column in enumerate(self.target_blocks):
            for y, block in enumerate(column):
                if block == target_block:
                    return x, y
        raise Exception(f"Target block at ({target_block.pos.x}, {target_block.pos.y}) not found.")

    def add_target_block(self,
                         grid_coordinates: tuple[int, int],
                         creation_position: tuple[int, int],
                         y_destination: tuple[float, float] = None):
        selection_value = random()
        block_choice = block_table[-1][1]
        for weight, block in block_table:
            if selection_value < weight:
                block_choice = block
                break
        new_block = block_choice(creation_position, self.block_size, y_destination=y_destination)
        self.target_blocks[grid_coordinates[0]][grid_coordinates[1]] = new_block

    def target_hit_by_ball(self,
                           block: TargetBlock):
        # TODO Remove block from targets and add to falling, create an entry for block to drop and start timer

    def update(self):
        self.target_manager.update()
        self.falling_manager.update()

    def draw(self):
        self.target_manager.draw()
        self.falling_manager.draw()
