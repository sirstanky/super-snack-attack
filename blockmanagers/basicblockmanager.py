from pygame import Surface

from objects.blocks.basicblocks.basicblock import BasicBlock


class BasicBlockManager:
    def __init__(self,
                 blocks: list[BasicBlock] = None):
        if blocks is None:
            self._blocks: list[BasicBlock] = []
        else:
            self._blocks = blocks

    @property
    def blocks(self):
        return self._blocks

    def get_blocks(self):
        return self._blocks

    def get_block(self,
                  index: int):
        return self._blocks[index]

    def get_block_position(self,
                           block: BasicBlock):
        try:
            return self._blocks.index(block)
        except ValueError:
            return False

    def set_block(self,
                  block: BasicBlock,
                  index: int):
        self._blocks[index] = block

    def add_block(self,
                  block: BasicBlock):
        self._blocks.append(block)

    def remove_block(self,
                     block: BasicBlock):
        self._blocks.remove(block)

    def update(self,
               *args):
        for block in self.get_blocks():
            block.update()

    def draw(self,
             window: Surface):
        for block in self.get_blocks():
            block.draw(window)
