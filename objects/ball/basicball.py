from objects.basicobject import BasicObject
from objects.position import Position


class BasicBall(BasicObject):
    def __init__(self,
                 center: tuple[float, float],
                 width: float,
                 color: tuple[int, int, int],
                 max_speed: float,
                 speed_x: float = None,
                 speed_y: float = None,
                 going_up: bool = True,
                 going_right: bool = True):
        if speed_x is not None and speed_y is None:
            speed_y = self.get_other_vector(speed_x)
        elif speed_y is not None and speed_x is None:
            speed_x = self.get_other_vector(speed_y)
        elif speed_x is None and speed_y is None:
            speed_x, speed_y = 0.0, 0.0
        speed_x *= 1 if going_right else -1
        speed_y *= -1 if going_up else 1

        super().__init__(center,
                         (width, width),
                         color,
                         max_speed,
                         speed=(speed_x, speed_y))

        self.radius = self.pos.width / 2

    @BasicObject.speed_x.setter
    def speed_x(self,
                new_speed_x: float):
        self._speed[0] = new_speed_x
        adj = 1 if self._speed[1] > 0 else -1
        self._speed[1] = self.get_other_vector(new_speed_x) * adj

    @BasicObject.speed_y.setter
    def speed_y(self,
                new_speed_y: float):
        self._speed[1] = new_speed_y
        adj = 1 if self._speed[0] > 0 else -1
        self._speed[0] = self.get_other_vector(new_speed_y) * adj

    def get_collision(self,
                      check_obj: BasicObject | Position,
                      speed_factor: float = 1.0,
                      deflate: bool = False):
        """
        Checks all sides of a given objects position to detect a collision.

        :param check_obj: object to check for collision
        :return: percentage of frame moved before collision and the int side of collision, or None
        """
        def get_collide_distance(point_speed: tuple[float, float],
                                 line: tuple[tuple[float, float], tuple[float, float]],
                                 line_speed: tuple[float, float]):
            l1, l2 = line
            if l1[1] == l2[1]:
                if -(point_speed[1] - line_speed[1]) == 0:
                    return None
                t = (self.pos.y - l1[1]) / -(point_speed[1] - line_speed[1])
            else:
                if -(point_speed[0] - line_speed[0]) == 0:
                    return None
                t = (self.pos.x - l1[0]) / -(point_speed[0] - line_speed[0])
            return t if 0 < t <= 1 else None

        def partial_move(point_speed: tuple[float, float],
                         line: tuple[tuple[float, float], tuple[float, float]],
                         line_speed: tuple[float, float],
                         move_factor: float):
            px, py = point_speed
            p = round(self.pos.x + (px * move_factor), 3), round(self.pos.y + (py * move_factor), 3)
            l1, l2 = line
            lx, ly = line_speed
            l1 = round(l1[0] + (lx * move_factor), 3), round(l1[1] + (ly * move_factor), 3)
            l2 = round(l2[0] + (lx * move_factor), 3), round(l2[1] + (ly * move_factor), 3)
            l = l1, l2
            return p, l

        def is_point_on_line(point: tuple[float, float],
                             line: tuple[tuple[float, float], tuple[float, float]]):
            l1, l2 = line
            if l1[1] == l2[1]:
                if point[1] == l1[1] and min(l1[0], l2[0]) <= point[0] <= max(l1[0], l2[0]):
                    return True
            elif point[0] == l1[0] and min(l1[1], l2[1]) <= point[1] <= max(l1[1], l2[1]):
                return True
            return False

        if isinstance(check_obj, BasicObject):
            if not deflate:
                r = check_obj.pos.inflate(self.pos.size)
            else:
                r = check_obj.pos.deflate(self.pos.size)
            rsx = check_obj.speed_x
            rsy = check_obj.speed_y
        else:
            if not deflate:
                r = check_obj.inflate(self.pos.size)
            else:
                r = check_obj.deflate(self.pos.size)
            rsx = 0
            rsy = 0
        speed_x = self.speed_x * speed_factor
        speed_y = self.speed_y * speed_factor
        edges = [r.top_edge, r.right_edge, r.bottom_edge, r.left_edge]
        shortest_dist = float('inf')
        closest_side = None
        for i, edge in enumerate(edges):
            dist = get_collide_distance((speed_x, speed_y), edge, (rsx, rsy))
            if dist:
                new_point, new_line = partial_move((speed_x, speed_y), edge, (rsx, rsy), dist)
                if is_point_on_line(new_point, new_line):
                    if dist < shortest_dist:
                        shortest_dist = dist
                        closest_side = i
        if closest_side is not None:
            return shortest_dist, closest_side
        else:
            return None, None
