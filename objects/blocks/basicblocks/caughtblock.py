from objects.blocks.basicblocks.block import Block


class CaughtBlock(Block):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 color: tuple[int, int, int]):
        super().__init__(center,
                         size,
                         color,
                         0.0)

    def update(self,
               position: tuple[float, float]):
        self.pos.center = position
