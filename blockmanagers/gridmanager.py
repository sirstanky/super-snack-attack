from blockmanagers.basicblockmanager import BasicBlockManager
from objects.blocks.basicblocks.block import Block


class GridManager(BasicBlockManager):
    def __init__(self,
                 size: int = None,
                 blocks: list[Block | None] = None):
        if blocks is None:
            if size is None:
                raise Exception("GridManager not properly initialized (no size or block list provided).")
            blocks = [None] * size

        super().__init__(blocks)

    def get_blocks(self):
        return [_ for _ in super().get_blocks() if _ is not None]

    def get_first_none(self):
        index = None
        for i in range(len(self._blocks)):
            if self._blocks[i] is None:
                index = i
            else:
                break
        return index

    def add_block_at_index(self,
                           block: Block,
                           index: int):
        self.set_block(block, index)

    def remove_block(self,
                     block: Block):
        try:
            self._blocks[self._blocks.index(block)] = None
            return True
        except ValueError:
            return False

    def shift_blocks_down(self):
        blocks, nones = [], []
        for block in self._blocks:
            if block is not None:
                blocks.append(block)
            else:
                nones.append(None)
        self._blocks = nones + blocks

