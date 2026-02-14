"""
Provides utility functions and classes for the OceanMining game.
"""

from seamaster.models.point import Point
from seamaster.constants import Direction


def manhattan_distance(p1: Point, p2: Point) -> int:
    """
    Calculate the Manhattan distance between two points.
    Args:
        p1 (Point): The first point.
        p2 (Point): The second point.
    Returns:
        int: The Manhattan distance between p1 and p2.
    """
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def next_point(p: Point, d: Direction):
    """
    Get the next point in the specified direction.
    Args:
        p (Point): The current point.
        d (Direction): The direction to move.
    Returns:
        Point: The next point in the specified direction.
    """
    if d == Direction.NORTH and p.y + 1 >= 0 and p.y + 1 < 20:
        return Point(p.x, p.y + 1)
    if d == Direction.SOUTH and p.y - 1 >= 0 and p.y - 1 < 20:
        return Point(p.x, p.y - 1)
    if d == Direction.EAST and p.x + 1 >= 0 and p.x + 1 < 20:
        return Point(p.x + 1, p.y)
    if d == Direction.WEST and p.x - 1 >= 0 and p.x - 1 < 20:
        return Point(p.x - 1, p.y)


def direction_from_point(p1: Point, p2: Point) -> Direction:
    """
    Get the primary cardinal direction from p1 to p2.
    Args:
        p1 (Point): The starting point.
        p2 (Point): The target point.
    Returns:
        Direction: The primary cardinal direction from p1 to p2.
    Raises:
        ValueError: If either point is out of bounds.
    """
    if (
        p1.x > 20
        or p1.x < 0
        or p1.y > 20
        or p1.y < 0
        or p2.x > 20
        or p2.x < 0
        or p2.y > 20
        or p2.y < 0
    ):
        raise ValueError(
            "Points must be within the grid bounds (0-19 for both x and y)"
        )
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    if abs(dx) >= abs(dy):
        return Direction.EAST if dx > 0 else Direction.WEST
    return Direction.NORTH if dy > 0 else Direction.SOUTH


class BotIDAllocator:
    """
    bot ID generator.
    """

    def __init__(self, start: int = 1):
        self._next_id = start

    def allocate(self) -> int:
        """
        Allocate and return the next available bot ID.
        """
        bot_id = self._next_id
        self._next_id += 1
        return bot_id
