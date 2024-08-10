from random import random

import constants as c
from objects.blocks.basicblocks.block import Block
from objects.blocks.cheese import Cheese
from objects.blocks.lettuce import Lettuce
from objects.paddle.catcher import Catcher
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
        self.drop_block_timers: list[tuple[Timer, int]] = []
        self.target_blocks: list[list[Block]] = [[Cheese(self.target_positions[x][y], self.block_size)
                                                 for y in range(self.target_rows)]
                                                 for x in range(self.target_columns)]
        self.falling_blocks: list[Block] = []
        self.caught_blocks: list[Block] = []

        self.catcher = Catcher()

    def get_all_target_blocks(self):
        target_blocks = []
        for column in range(len(self.target_blocks)):
            target_blocks += self.get_target_blocks_in_column(column)
        return target_blocks

    def get_target_blocks_in_column(self,
                                    column: int):
        return [block for block in self.target_blocks[column] if block is not None]

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

    def get_first_none(self,
                       column: int):
        index = None
        for i in range(len(self.target_blocks[column])):
            if self.target_blocks[column][i] is None:
                index = i
            else:
                break
        return index

    def target_hit_by_ball(self,
                           block: Block):
        for col_num, column in enumerate(self.target_blocks):
            if block in column:
                column.remove(block)
                timer = Timer(c.target_manager_drop_delay)
                self.drop_block_timers.append((timer, col_num))
                timer.start()
                self.shift_blocks_down(col_num)
                self.falling_blocks.append(block)
                block.change_state(Block.State.FALLING)
                break

    def shift_blocks_down(self,
                          column: int):
        blocks, nones = [], []
        for block in self.target_blocks[column]:
            if block is not None:
                blocks.append(block)
            else:
                nones.append(None)
        self.target_blocks[column] = nones + blocks
        for block in self.get_target_blocks_in_column(column):
            x, y = self.get_target_block_coordinate(block)
            block.y_destination = self.drop_positions[x][y][1]

    def get_lowest_falling_block(self):
        cut_off_y = self.catcher.pos.y if not self.caught_blocks else self.caught_blocks[-1].pos.bottom
        lowest_block = None
        lowest_y = 0
        for block in self.falling_blocks:
            if lowest_y < block.pos.bottom < cut_off_y:
                lowest_y = block.pos.bottom
                lowest_block = block
        return lowest_block

    def update(self):
        for timer, column in self.drop_block_timers:
            timer.update()
            row = self.get_first_none(column)
            if row is not None and timer.expired:
                self.add_target_block((column, row), self.drop_positions[column][row],
                                      y_destination=self.target_positions[column][row])
                self.drop_block_timers.remove((timer, column))
        for block in self.get_all_target_blocks():
            block.update()
        for block in self.falling_blocks:
            block.update()
            if block.pos.top > c.window_height:
                self.falling_blocks.remove(block)
        lowest_block = self.get_lowest_falling_block()
        accelerate = (0, 0)
        if lowest_block:
            if not lowest_block.pos.left < self.catcher.pos.x < lowest_block.pos.right:
                if self.catcher.pos.x < lowest_block.pos.left:
                    accelerate = (1, 0)
                else:
                    accelerate = (-1, 0)
        self.catcher.accelerate(accelerate)
        self.catcher.update()
        for index, block in self.caught_blocks:
            block.update(cather_position=self.catcher.pos, layer=index)

    def draw(self):
        self.catcher.draw()
        for block in (self.get_all_target_blocks() + self.falling_blocks + self.caught_blocks):
            block.draw()
