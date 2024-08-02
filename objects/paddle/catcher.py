import constants as c
from objects.blocks.basicblocks.caughtblock import CaughtBlock
from blockmanagers.caughtblockmanager import CaughtBlockManager
from blockmanagers.fallingblockmanager import FallingBlockManager
from objects.paddle.paddle import Paddle
from objects.position import Position


class Catcher(Paddle):
    def __init__(self,
                 center: tuple[float, float] = None,
                 size: tuple[float, float] = None,
                 color: tuple[int, int, int] = (0, 255, 0),
                 max_speed: float = None,
                 acceleration: float = None):
        if center is None:
            center = (c.window_width / 2, c.window_height * 0.95)
        if size is None:
            size = c.catcher_size
        if max_speed is None:
            max_speed = c.catcher_max_speed
        if acceleration is None:
            acceleration = c.catcher_acceleration

        super().__init__(center,
                         size,
                         color,
                         max_speed,
                         acceleration)

        self.cur_max_speed = self.max_speed
        self.caught_manager = CaughtBlockManager()

    @property
    def catch_area(self):
        if not self.caught_manager.blocks:
            return self.pos
        block = self.caught_manager.blocks[-1]
        return Position(block.pos.center, (block.pos.width, self.pos.height))

    def get_active_blocks(self):
        if len(self.caught_manager.blocks) > self.caught_manager.display_limit:
            return len(self.caught_manager.blocks) - self.caught_manager.display_limit
        return 0

    def update(self,
               falling_manager: FallingBlockManager):
        def catch_blocks():
            for block in falling_manager.blocks:
                if block.pos.collides_with_position(self.catch_area):
                    self.cur_max_speed = self.max_speed - (
                            (len(self.caught_manager.blocks) / self.caught_manager.display_limit) * self.max_speed)
                    if self.cur_max_speed < 0.51:
                        self.cur_max_speed = 0.51
                    self.caught_manager.blocks.append(CaughtBlock((0, 0), c.caught_block_size, block.color))
                    falling_manager.remove_block(block)

        def decide_movement():
            lowest_block = falling_manager.get_lowest_block(self.catch_area.bottom)
            accelerate = (0, 0)
            if lowest_block:
                if not lowest_block.pos.left < self.pos.x < lowest_block.pos.right:
                    if self.pos.x < lowest_block.pos.left:
                        accelerate = (1, 0)
                    else:
                        accelerate = (-1, 0)
            self.accelerate(accelerate)

        def update_blocks():
            for index, block in enumerate(self.caught_manager.blocks[self.get_active_blocks():]):
                y = self.pos.top - (block.pos.height / 2) * (index + 1)
                block.update((self.pos.x, y))

        catch_blocks()
        decide_movement()
        super().update()
        update_blocks()

    def draw(self):
        super().draw()
        for block in self.caught_manager.blocks[self.get_active_blocks():]:
            block.draw()
