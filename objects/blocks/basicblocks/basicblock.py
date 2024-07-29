from objects.basicobject import BasicObject


class BasicBlock(BasicObject):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 color: tuple[int, int, int],
                 max_speed: float,
                 speed: tuple[float, float] = None,
                 acceleration: float = None):
        super().__init__(center,
                         size,
                         color,
                         max_speed,
                         speed=speed,
                         acceleration=acceleration)
