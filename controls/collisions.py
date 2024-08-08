from math import inf

import constants as c
from objects.basicobject import BasicObject
from objects.blocks.basicblocks.block import Block
from objects.position import Position


def inflate_collision_rect(obj: BasicObject,
                           collide_obj: BasicObject):
    center_x = (collide_obj.pos.x + collide_obj.prev_pos.x) / 2
    center_y = (collide_obj.pos.y + collide_obj.prev_pos.y) / 2
    width = max(collide_obj.pos.right, collide_obj.prev_pos.right) - min(collide_obj.pos.left, collide_obj.prev_pos.left)
    height = max(collide_obj.pos.bottom, collide_obj.prev_pos.bottom) - min(collide_obj.pos.top, collide_obj.prev_pos.top)
    width += obj.pos.width
    height += obj.pos.height
    return Position((center_x, center_y), (width, height))


def get_intersection_point(line: tuple[tuple[float, float], tuple[float, float]],
                           rect: Position):

    edges = [rect.top_edge, rect.right_edge, rect.bottom_edge, rect.left_edge]
    shortest_distance = inf
    closest_intersection = None
    edge_direction = None
    for direction, edge in enumerate(edges):
        intersection = line_intersects_line(line, edge)
        if intersection:
            new_distance = c.get_distance(line[0], intersection)
            if new_distance < shortest_distance:
                shortest_distance = new_distance
                closest_intersection = intersection
                edge_direction = direction
    return closest_intersection, edge_direction


def line_intersects_line(line_1: tuple[tuple[float, float], tuple[float, float]],
                         line_2: tuple[tuple[float, float], tuple[float, float]]):
    (x1, y1), (x2, y2) = line_1
    (x3, y3), (x4, y4) = line_2
    base = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if base == 0:
        return None
    intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / base
    intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / base
    point = (intersect_x, intersect_y)
    if point_on_line(point, line_1) and point_on_line(point, line_2):
        return intersect_x, intersect_y


def point_on_line(point: tuple[float, float],
                  line: tuple[tuple[float, float], tuple[float, float]]):
    px, py = round(point[0], 3), round(point[1], 3)
    (x1, y1), (x2, y2) = (round(line[0][0], 3), round(line[0][1], 3)), (round(line[1][0], 3), round(line[1][1], 3))
    return min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2)


def check_corner_collision(intersection_point: tuple[float, float],
                           rect: Position,
                           obj_speed: tuple[float, float]):
    if intersection_point == rect.top_left and (obj_speed[0] >= 0 and obj_speed[1] >= 0):
        return True
    elif intersection_point == rect.top_right and (obj_speed[0] <= 0 <= obj_speed[1]):
        return True
    elif intersection_point == rect.bottom_left and (obj_speed[0] >= 0 >= obj_speed[1]):
        return True
    elif intersection_point == rect.bottom_right and (obj_speed[0] <= 0 and obj_speed[1] <= 0):
        return True
    return False


def get_collision_with_closest_block(obj: BasicObject,
                                     blocks: list[Block]):

    closest_block = None
    closest_distance = inf
    closest_intersection = None
    collision_side = None
    for block in blocks:
        intersection, side = get_intersection_point(obj.trajectory, inflate_collision_rect(obj, block))
        if intersection:
            new_distance = c.get_distance(obj.prev_pos.center_line, intersection)
            if new_distance <= closest_distance:
                closest_distance = new_distance
                closest_block = block
                closest_intersection = intersection
                collision_side = side
    return closest_block, closest_intersection, collision_side
