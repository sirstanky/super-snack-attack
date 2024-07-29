from pygame import Surface

import constants as c
from blockmanagers.gridmanager import GridManager
from controls.timer import Timer
from objects.blocks.basicblocks.targetblock import TargetBlock


class TargetManager:
    def __init__(self,
                 grid_size: tuple[int, int]):
        columns, rows = grid_size
        self.num_columns = columns
        self.num_rows = rows

        # Setup block dimensions
        column_width = c.window_width / columns
        gap = column_width / 10
        block_width = column_width - gap
        block_height = ((c.target_area + c.top_window_ui_buffer) / rows) - gap
        self.block_size = (block_width, block_height)

        # Setup block positions on screen
        x = [int(((block_width + gap) * _ + (gap // 2)) + (block_width // 2)) for _ in range(columns)]
        y = [int(((block_height + gap) * _ + gap) + (block_height // 2) + c.top_window_ui_buffer) for _ in range(rows)]
        self.grid_positions = [[(x[i], y[j]) for j in range(rows)] for i in range(columns)]

        # Setup drop area above window
        drop_positions = [[(x[i], y[j]) for j in range(rows)] for i in range(columns)]
        for x in range(len(drop_positions)):
            for y in range(len(drop_positions[x])):
                drop_positions[x][y] = drop_positions[x][y][0], -drop_positions[x][y][1]
            drop_positions[x].reverse()
        self.drop_positions = drop_positions

        self.columns = [GridManager(rows, [
            TargetBlock(self.grid_positions[x][y], self.block_size) for y in range(rows)]) for x in range(columns)]

        self.block_drop_timers: dict[Timer, int] = {}
        self.aligned = True

    def get_all_blocks(self):
        all_blocks: list[TargetBlock] = []
        for column in self.columns:
            all_blocks += column.get_blocks()
        return all_blocks

    def get_block_position(self,
                           block: TargetBlock):
        for x, column in enumerate(self.columns):
            y = column.get_block_position(block)
            if y is not False:
                return x, y
        raise Exception("Coordinates for the block not found.")

    def add_block(self,
                  grid_position: tuple[int, int],
                  window_position: tuple[float, float] = None):
        if window_position is None:
            position = self.grid_positions[grid_position[0]][grid_position[1]]
            dest_y = None
        else:
            position = window_position
            dest_y = self.grid_positions[grid_position[0]][grid_position[1]][1]
        new_block = TargetBlock(position, self.block_size, dest_y=dest_y)
        self.columns[grid_position[0]].add_block_at_index(new_block, grid_position[1])

    def remove_block(self,
                     block: TargetBlock):
        for column in self.columns:
            if column.remove_block(block):
                timer = Timer(c.target_manager_drop_delay)
                timer.start()
                self.block_drop_timers[timer] = self.columns.index(column)
                self.shift_blocks_down(self.columns.index(column))
                return
        raise Exception("Block not found for removal.")

    def shift_blocks_down(self,
                          column: int):
        self.columns[column].shift_blocks_down()
        for block in self.columns[column].get_blocks():
            x, y = self.get_block_position(block)
            block.set_destination(self.grid_positions[x][y][1])

    def update_drop_timers(self):
        if not self.block_drop_timers:
            return
        for timer, column in self.block_drop_timers.items():
            timer.update()
            row = self.columns[column].get_first_none()
            if row is not None and timer.expired:
                self.add_block((column, row), self.drop_positions[column][row])
        self.block_drop_timers = {timer: self.block_drop_timers[timer] for timer in self.block_drop_timers if
                                  not timer.ready}

    def update(self):
        self.update_drop_timers()
        for block in self.get_all_blocks():
            block.update()

    def draw(self,
             window: Surface):
        for column in self.columns:
            column.draw(window)
