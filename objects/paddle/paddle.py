from objects.basicobject import BasicObject


class Paddle(BasicObject):
    def __init__(self,
                 center: tuple[float, float],
                 size: tuple[float, float],
                 color: tuple[int, int, int],
                 max_speed: float,
                 acceleration: float):
        super().__init__(center,
                         size,
                         color,
                         max_speed)

        self.acceleration = acceleration

    # def accelerate(self,
    #                direction: int):
    #     if self.speed_x != 0 and self.speed_x / abs(self.speed_x) != direction:
    #         acceleration = self.acceleration * 2
    #     else:
    #         acceleration = self.acceleration
    #     self.speed_x += self.max_speed * acceleration * direction
    #     if abs(self.speed_x) > self.max_speed:
    #         self.speed_x = self.max_speed * (self.speed_x / abs(self.speed_x))
    #
    # def decelerate(self):
    #     if self.speed_x == 0:
    #         return
    #     direction = self.speed_x / abs(self.speed_x)
    #     self.accelerate(-direction)
    #     if self.speed_x != 0 and self.speed_x / abs(self.speed_x) != direction:
    #         self.speed_x = 0

    def update(self,
               **kwargs):
        super().update()
