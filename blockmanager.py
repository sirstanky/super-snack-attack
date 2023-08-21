import constants as c
from ball import Ball
from block import Block, TargetBlock, CaughtBlock
from paddle import Catcher
from pygame import Rect, Surface
from random import randint


class BlockManager:

    def __init__(self, blocks):
        self.blocks = blocks

    def remove_block(self, block: Block):
        self.blocks.remove(block)

    def draw(self, window: Surface):
        for block in self.blocks:
            block.draw(window)


class FallingBlockManager(BlockManager):

    def __init__(self):
        self.color = (255, 0, 0)
        self.max_speed = 4.0
        super().__init__([])

    def add_block(self, block: Block):
        self.blocks.append(Block(block.pos.x, block.pos.y, block.pos.w, block.pos.h, block.color, self.max_speed))
        self.blocks[-1].speed_y = self.max_speed

    def get_lowest_block(self, limit: int):

        if self.blocks:
            lowest_block = None
            lowest_y = 0
            for block in self.blocks:
                if lowest_y < block.pos.centery < limit:
                    lowest_y = block.pos.bottom
                    lowest_block = block
            if lowest_block is not None:
                return lowest_block.pos.centerx
        else:
            return None

    def update(self):

        for block in self.blocks:
            block.update()
            # Falls below the screen
            if block.pos.y > c.window_height:
                self.remove_block(block)


class CaughtBlockManager(BlockManager):

    def __init__(self):
        self.catcher = Catcher()
        self.catch_area = Rect(self.catcher.pos.x, self.catcher.pos.y,
                               self.catcher.pos.width, self.catcher.pos.height)
        self.catch_limit = 20
        self.block_reserve: list[CaughtBlock] = []
        self.block_width = self.catcher.pos.width * 1.2
        self.block_height = self.catcher.pos.height / 4
        self.x_offset = (self.block_width - self.catcher.pos.width) / 2
        self.color = (255, 0, 0)
        super().__init__([])

    def add_block(self, block: Block):
        self.blocks.append(CaughtBlock(self.catcher.pos.midtop, len(self.blocks),
                                       self.block_width, self.block_height, color=block.color))

    def catch_block(self, block: Block, falling_manager: FallingBlockManager):
        falling_manager.remove_block(block)
        self.add_block(block)
        if len(self.blocks) > self.catch_limit:
            self.block_reserve.append(self.blocks.pop(0))

    def fill_blocks(self):

        i = 0
        while i < len(self.block_reserve) and len(self.blocks) <= self.catch_limit:
            self.blocks.insert(0, self.block_reserve.pop(-1))
            i += 1

    def update(self, falling_manager: FallingBlockManager):

        # Update catch area
        if self.blocks:
            self.catch_area.topleft = self.blocks[-1].pos.topleft
            self.catch_area.width = self.blocks[-1].pos.width
        else:
            self.catch_area.topleft = self.catcher.pos.topleft
            self.catch_area.width = self.catcher.pos.width

        self.catcher.update(len(self.blocks), self.catch_limit,
                            falling_manager.get_lowest_block(self.catch_area.bottom))

        # Check for caught blocks
        for block in falling_manager.blocks:
            if block.pos.colliderect(self.catch_area) and block.get_collision_direction(self.catch_area) == 's':
                self.catch_block(block, falling_manager)

        # Fill blocks from reserves
        if self.block_reserve and len(self.blocks) < self.catch_limit:
            self.fill_blocks()

        # Position blocks to follow catcher
        for index, block in enumerate(self.blocks):
            block.update(self.catcher.pos.midtop, index)

    def draw(self, window):
        self.catcher.draw(window)
        super().draw(window)


class TargetManager:

    def __init__(self, rows: int, columns: int):

        # Flags
        self.new_rows_queue: list[list[BlockManager, int]] = []
        self.new_row_delay = False

        # Setup block dimensions
        column_width = c.window_width / columns
        self.rows = rows
        self.columns = columns
        self.gap = column_width / 10
        self.block_width = column_width - self.gap
        self.block_height = ((c.window_height * c.target_area) / rows) - self.gap

        # Create all target blocks
        self.blocks: list[list[BlockManager, int]] = [[BlockManager(self.make_new_row(row)), index] for index, row in
                                                      enumerate(range(rows))]

    def make_new_row(self, row: int):
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        return [TargetBlock(row, column, self.block_width, self.block_height, self.gap, color)
                for column in range(self.columns)]

    def shift_blocks_down(self, row_limit=c.window_height):

        for row in self.blocks:
            block_manager, index = row
            if index < row_limit:
                row[1] += 1
                for block in block_manager.blocks:
                    block.row += 1
                    self.update_block_pos(block)

    def update_block_pos(self, block: TargetBlock):
        block.pos.x = ((block.pos.width + self.gap) * block.column) + (self.gap / 2)
        block.pos.y = ((self.block_height + self.gap) * block.row) + self.gap

    def remove_block(self, block: Block):

        # Returns True if the row is left empty
        for row in self.blocks:
            if block in row[0].blocks:
                row[0].remove_block(block)
            # Check if row is empty
            if not row[0].blocks:
                self.blocks.remove(row)
                return True
        return False

    def update(self, ball: Ball, falling_manager: FallingBlockManager):

        # TODO Clean this up; it's very dirty. Maybe don't use 'remove_block' to check for empty rows.
        for row in self.blocks:
            for block in row[0].blocks:
                if block.update(ball):
                    falling_manager.add_block(block)
                    if self.remove_block(block):
                        self.new_rows_queue.append([BlockManager(self.make_new_row(0)), row[1]])

        # Create a new row once the ball is out of the way
        if len(self.new_rows_queue) > 0:
            if not ball.pos.colliderect(0, 0, c.window_width, c.window_height * c.target_area):
                new_blocks, row_limit = self.new_rows_queue.pop(0)
                self.shift_blocks_down(row_limit)
                self.blocks.append([new_blocks, 0])
                if len(self.new_rows_queue) > 0:
                    for row in self.new_rows_queue:
                        row[1] += 1

    def draw(self, window: Surface):

        for row in self.blocks:
            for block in row[0].blocks:
                block.draw(window)
